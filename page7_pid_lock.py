"""Streamlit app: interactive PID dither-lock simulation.

Run with:
    streamlit run streamlit_pid_lock.py

The animation is rendered directly in the browser via matplotlib's
JS-HTML embedding (``anim.to_jshtml``); no .mp4 or .gif files are written.
"""

from re import U
import matplotlib

matplotlib.use("Agg")  # headless backend, no GUI window

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from matplotlib.animation import FuncAnimation
from pid_lock_module import cavity_transmission, create_simulation

# Allow large inline animations to be embedded as HTML/JS.
plt.rcParams["animation.embed_limit"] = 200  # MB


def build_animation(p):
    """Build the matplotlib FuncAnimation for the given parameters."""
    t, f_free_running, f_locked, filtered_error_hist = create_simulation(p)
    t_ms = t * 1e3

    fig, (ax_top, ax_mid, ax_bot) = plt.subplots(3, 1, figsize=(10, 11))
    fig.suptitle("PID servo locking the laser to the cavity")
    fig.subplots_adjust(bottom=0.07, hspace=0.35)

    # Top panel: cavity peak + current laser position homing onto resonance.
    f_axis = np.linspace(-20, max(f_free_running.max(), f_locked.max()) + 5, 600)
    ax_top.plot(
        f_axis,
        cavity_transmission(f_axis, p["cavity_center"], p["cavity_fwhm"], p["cavity_port"]),
        color="black",
        lw=2,
        label="Cavity Transmission (lock target)",
    )
    dither_span = ax_top.axvspan(0, 0, color="green", alpha=0.15, label="Dither excursion")
    (laser_pt,) = ax_top.plot([], [], "o", color="green", ms=10, label="Laser frequency")
    laser_line = ax_top.axvline(0, color="green", ls="--", alpha=0.6)
    ax_top.axvline(p["cavity_center"], color="gray", linestyle="--", alpha=0.3)
    ax_top.set_xlabel("Laser Frequency Detuning (MHz)")
    ax_top.set_ylabel("Transmission")
    ax_top.set_xlim(f_axis[0], f_axis[-1])
    ax_top.set_ylim(-0.05, 1.1)
    ax_top.legend(loc="upper right")
    ax_top.grid(True, alpha=0.3)

    # Middle panel: laser frequency vs time (unlocked vs locked).
    (free_curve,) = ax_mid.plot(
        [], [], color="gray", linestyle=":", lw=2, label="Unlocked Laser (Drifting)"
    )
    (locked_curve,) = ax_mid.plot([], [], color="green", lw=2, label="Laser Frequency (Servo)")
    (locked_pt,) = ax_mid.plot([], [], "o", color="green", ms=8)
    ax_mid.axhline(p["cavity_center"], color="black", linestyle="-", lw=1, label="Target Cavity Peak")
    ax_mid.axvline(p["lock_on_time"] * 1e3, color="red", linestyle="--", label="Servo ON")
    ax_mid.set_xlabel("Time (ms)")
    ax_mid.set_ylabel("Laser Frequency (MHz)")
    ax_mid.set_xlim(t_ms[0], t_ms[-1])
    f_lo = min(f_free_running.min(), f_locked.min()) - 2
    f_hi = max(f_free_running.max(), f_locked.max()) + 2
    ax_mid.set_ylim(f_lo, f_hi)
    ax_mid.legend(loc="upper right")
    ax_mid.grid(True, alpha=0.3)

    # Bottom panel: filtered (demodulated) error signal vs time.
    (error_curve,) = ax_bot.plot(
        [], [], color="purple", lw=2, label="filtered_error (servo input)"
    )
    (error_pt,) = ax_bot.plot([], [], "o", color="purple", ms=8)
    ax_bot.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax_bot.axvline(p["lock_on_time"] * 1e3, color="red", linestyle="--", label="Servo ON")
    ax_bot.set_xlabel("Time (ms)")
    ax_bot.set_ylabel("Filtered Error Signal")
    ax_bot.set_xlim(t_ms[0], t_ms[-1])
    err_pad = 0.1 * (np.max(np.abs(filtered_error_hist)) + 1e-9)
    ax_bot.set_ylim(filtered_error_hist.min() - err_pad, filtered_error_hist.max() + err_pad)
    ax_bot.legend(loc="upper right")
    ax_bot.grid(True, alpha=0.3)

    frames = range(0, len(t), p["frame_step"])

    def update(i):
        f = f_locked[i]
        lo, hi = f - p["dither_amp"], f + p["dither_amp"]
        dither_span.set_x(lo)
        dither_span.set_width(hi - lo)
        laser_line.set_xdata([f, f])
        laser_pt.set_data(
            [f], [cavity_transmission(f, p["cavity_center"], p["cavity_fwhm"], p["cavity_port"])]
        )

        free_curve.set_data(t_ms[: i + 1], f_free_running[: i + 1])
        locked_curve.set_data(t_ms[: i + 1], f_locked[: i + 1])
        locked_pt.set_data([t_ms[i]], [f_locked[i]])
        ax_mid.set_title(f"Servo Response at t = {t_ms[i]:.2f} ms")

        error_curve.set_data(t_ms[: i + 1], filtered_error_hist[: i + 1])
        error_pt.set_data([t_ms[i]], [filtered_error_hist[i]])
        return (
            dither_span,
            laser_line,
            laser_pt,
            free_curve,
            locked_curve,
            locked_pt,
            error_curve,
            error_pt,
        )

    anim = FuncAnimation(
        fig, update, frames=frames, interval=1000 / p["fps"], blit=False
    )
    return fig, anim


# ==========================================
# Streamlit UI
# ==========================================
st.set_page_config(page_title="PID Dither-Lock Simulator", layout="wide")
st.title("PID Dither-Lock Simulator")
st.write(
    "Interactive simulation of a laser frequency locked to a reference cavity "
    "using dither modulation and a PID servo. Set the parameters and run."
)

with st.sidebar:
    st.header("Cavity")
    cavity_center = st.number_input("Cavity center (MHz)", value=0.0, step=1.0)
    cavity_fwhm = st.number_input("Cavity FWHM (MHz)", value=10.0, min_value=0.1, step=0.5)
    cavity_port = st.selectbox(
        "Cavity port", options=["return", "through"], index=0,
        help="'return' = reflection dip (peak inverted); 'through' = transmission peak.",
    )

    st.header("Dither")
    dither_freq = st.number_input("Dither frequency (Hz)", value=5000.0, min_value=1.0, step=100.0)
    dither_amp_frac = st.slider(
        "Dither amplitude (fraction of FWHM)", min_value=0.01, max_value=1.0, value=0.2, step=0.01
    )

    st.header("PID servo")
    Kp = st.number_input("Kp (proportional gain)", value=0.5, step=0.1, format="%.3f")
    Ki = st.number_input("Ki (integral gain)", value=50.0, step=1.0, format="%.3f")
    lpf_alpha = st.slider("LPF alpha (low-pass coeff.)", min_value=0.001, max_value=1.0, value=0.01, step=0.001)
    lock_on_time_ms = st.number_input("Servo ON time (ms)", value=15.0, min_value=0.0, step=1.0)

    st.header("Laser drift")
    drift_offset = st.number_input("Initial offset (MHz)", value=10.0, step=1.0)
    drift_slope = st.number_input("Drift slope (MHz/s)", value=50.0, step=5.0)
    noise_amp = st.number_input("Random-walk noise amplitude", value=0.1, min_value=0.0, step=0.05, format="%.3f")
    seed = st.number_input("Random seed", value=0, min_value=0, step=1)

    st.header("Simulation / playback")
    t_total_ms = st.number_input("Total time (ms)", value=30.0, min_value=1.0, step=5.0)
    dt_ms = st.number_input("Time step dt (ms)", value=0.01, min_value=0.001, step=0.005, format="%.3f")
    frame_step = st.number_input(
        "Frame step (subsample)", value=25, min_value=1, step=1,
        help="Plot every Nth simulation step as an animation frame.",
    )
    fps = st.number_input("Playback FPS", value=20, min_value=1, max_value=60, step=1)

run = st.button("Create simulation", type="primary")

if run:
    params = {
        "cavity_center": cavity_center,
        "cavity_fwhm": cavity_fwhm,
        "cavity_port": cavity_port,
        "dither_freq": dither_freq,
        "dither_amp": dither_amp_frac * cavity_fwhm,
        "Kp": Kp,
        "Ki": Ki,
        "lpf_alpha": lpf_alpha,
        "lock_on_time": lock_on_time_ms * 1e-3,
        "drift_offset": drift_offset,
        "drift_slope": drift_slope,
        "noise_amp": noise_amp,
        "seed": int(seed),
        "t_total": t_total_ms * 1e-3,
        "dt": dt_ms * 1e-3,
        "frame_step": int(frame_step),
        "fps": int(fps),
    }

    with st.spinner("Running simulation and rendering animation..."):
        fig, anim = build_animation(params)
        html = anim.to_jshtml()
        plt.close(fig)

    components.html(
        html,
        height=1500,
        scrolling=True
        )
else:
    st.info("Adjust parameters in the sidebar, then click **Run simulation**.")

st.divider()

with open('pid_lock_module.py', 'r') as f:
    code_display = f.read()
with st.expander(label="`pid_lock_module.py`", expanded=False):
    st.code(code_display, language = 'python')
