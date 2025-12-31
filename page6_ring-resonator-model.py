import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Ring Resonator Model", page_icon="🔄", layout="wide")

st.header("Ring Resonator Model")
st.divider()

# Default resonance frequency for Q calculations (193 THz = telecom wavelength)
OMEGA_M_DEFAULT = 193e12 * 2 * np.pi  # rad/s

# Sidebar for parameter sliders
with st.sidebar:
    st.subheader("Model Parameters")
    
    # Ring parameters
    st.markdown("### Ring Parameters")
    a = st.slider("a (Ring transmission magnitude)", 0.8, 1.0, 0.95, 0.01)
    sigma = st.slider("σ (Coupler transmission coefficient)", 0.5, 1.0, 0.9, 0.01)
    
    # Frequency parameters
    st.markdown("### Frequency Parameters")
    f_delta = st.slider("f_delta (Δf, splitting distance) (GHz)", 0.0, 10.0, 0.0, 0.01,
                        help="Splitting distance between Lorentzian peaks. Used to calculate phi_a = π * (f_delta / FSR_ring)")
    f_offset_min = st.number_input("Frequency offset min (GHz)", value=-5.0, step=0.1,
                                    help="Minimum frequency offset (f - f₀) for plotting")
    f_offset_max = st.number_input("Frequency offset max (GHz)", value=5.0, step=0.1,
                                    help="Maximum frequency offset (f - f₀) for plotting")
    f_FSRring = st.slider("FSR_ring (GHz)", 1.0, 100.0, 10.0, 0.1)
    f_FSRfp = st.slider("FSR_fp (GHz)", 1.0, 100.0, 10.0, 0.1)
    
    # Facet parameters
    st.markdown("### Facet Parameters")
    r = st.slider("r (Facet reflectivity)", 0.0, 0.5, 0.1, 0.01)
    t_fp = st.slider("t_fp (Fabry-Pérot transmission)", 0.5, 1.0, 0.9, 0.01)
    
    # Phase parameters
    st.markdown("### Phase Parameters")
    delta = st.slider("δ (Phase difference)", 0.0, 2.0 * np.pi, 0.0, 0.1)
    
    # Insertion loss parameters
    st.markdown("### Insertion Loss")
    IL_t = st.slider("IL_t (Transmission insertion loss)", 0.5, 1.0, 1.0, 0.01)
    IL_r = st.slider("IL_r (Reflection insertion loss)", 0.5, 1.0, 1.0, 0.01)

# Generate frequency offset range for plotting
f_offset = np.linspace(f_offset_min, f_offset_max, 1000)  # GHz (f - f₀)

# Calculate intermediate parameters
# phi_a from user's clarification: phi_a = pi * (f_delta / FSR_ring)
# where f_delta is the splitting distance (Delta f)
phi_a = np.pi * (f_delta / f_FSRring)

# Calculate tau and |rho| from a and phi_a
# From: a = sqrt(tau^2 + |rho|^2) and phi_a = arctan(|rho|/tau)
# tau = a * cos(phi_a), |rho| = a * sin(phi_a)
# phi_a is constant (from splitting distance), so tau and |rho| are constants
tau = a * np.cos(phi_a)
rho_mag = a * np.sin(phi_a)  # |rho|, assuming phi_e = 0 so rho is real

# Ring phase: phi_r = 2*pi * (f_offset / FSR_ring) - varies with frequency offset
phi_r = 2 * np.pi * (f_offset / f_FSRring)

# Calculate a_± = a * e^(±i*phi_a) * e^(i*phi_r)
a_plus = a * np.exp(1j * phi_a) * np.exp(1j * phi_r)
a_minus = a * np.exp(-1j * phi_a) * np.exp(1j * phi_r)

# Fabry-Pérot phase: phi_fp = phi_1 + phi_2
# From the doc: phi_1 + phi_2 = pi * (f - f_0) / FSR_fp + phi_s
# For simplicity, we use: phi_fp = pi * (f_offset / FSR_fp)
phi_fp = np.pi * (f_offset / f_FSRfp)

# Calculate transmission amplitude and effective reflectivity
A_t = IL_t * (1 - r**2)**2 * t_fp**4
r_e = r * t_fp**2

# Calculate T_full using the simplified equation (line 57)
# T_full = (A_t/4) * |numerator/denominator|^2
# numerator = (1 - sigma*a_+)(sigma - a_-) + (1 - sigma*a_-)(sigma - a_+)
# denominator = (1 - sigma*a_+)(1 - sigma*a_-) + r_e^2*(sigma - a_+)(sigma - a_-)*e^(i*2*phi_fp) 
#              - r_e*(1 - sigma^2)*|rho|*e^(i*(phi_r + phi_fp))*2*cos(delta)

numerator = (1 - sigma * a_plus) * (sigma - a_minus) + (1 - sigma * a_minus) * (sigma - a_plus)
denominator = (1 - sigma * a_plus) * (1 - sigma * a_minus) + \
              r_e**2 * (sigma - a_plus) * (sigma - a_minus) * np.exp(1j * 2 * phi_fp) - \
              r_e * (1 - sigma**2) * rho_mag * np.exp(1j * (phi_r + phi_fp)) * 2 * np.cos(delta)

T_full = (A_t / 4) * np.abs(numerator / denominator)**2

# Calculate quality factors
# Delta_omega_FSR = 2*pi*FSR_ring (convert GHz to rad/s)
Delta_omega_FSR = 2 * np.pi * f_FSRring * 1e9  # rad/s

# Use values at resonance (f_delta = 0) for Q calculations
# At resonance: phi_a = 0, so tau = a, |rho| = 0
# But we need to use the actual a and sigma values
# Q calculations use natural log, need to handle edge cases
sigma_a = sigma * a
if sigma_a > 0 and sigma_a < 1:
    Q_load = -OMEGA_M_DEFAULT / Delta_omega_FSR * np.pi / np.log(sigma_a)
else:
    Q_load = np.nan

if sigma > 0 and sigma < 1:
    Q_ext = -OMEGA_M_DEFAULT / Delta_omega_FSR * np.pi / np.log(sigma)
else:
    Q_ext = np.nan

if a > 0 and a < 1:
    Q_int = -OMEGA_M_DEFAULT / Delta_omega_FSR * np.pi / np.log(a)
else:
    Q_int = np.nan

# Escape efficiency
if sigma_a > 0 and sigma_a < 1 and sigma > 0 and sigma < 1:
    eta_esc = np.log(sigma) / np.log(sigma_a)
else:
    eta_esc = np.nan

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Transmission (T_full)")
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=f_offset,
        y=T_full,
        mode='lines',
        line=dict(color='blue', width=2),
        name='T_full'
    ))
    
    fig.update_traces(
        hovertemplate='Frequency offset: %{x:.3f} GHz<br>Transmission: %{y:.6f}<extra></extra>'
    )
    
    fig.update_layout(
        title='Transmission vs Frequency Offset',
        xaxis_title='Frequency Offset (f - f₀) [GHz]',
        yaxis_title='Transmission',
        template='plotly_white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Derived Metrics")
    
    st.markdown("### Quality Factors")
    if not np.isnan(Q_load):
        st.metric("Loaded Q", f"{Q_load/1e6:.2f} M", help="Q_load = -ω_m/(Δω_FSR) * π/ln(σa)")
    else:
        st.write("Loaded Q: Invalid (check parameters)")
    
    if not np.isnan(Q_ext):
        st.metric("Extrinsic Q", f"{Q_ext/1e6:.2f} M", help="Q_ext = -ω_m/(Δω_FSR) * π/ln(σ)")
    else:
        st.write("Extrinsic Q: Invalid (check parameters)")
    
    if not np.isnan(Q_int):
        st.metric("Intrinsic Q", f"{Q_int/1e6:.2f} M", help="Q_int = -ω_m/(Δω_FSR) * π/ln(a)")
    else:
        st.write("Intrinsic Q: Invalid (check parameters)")
    
    st.divider()
    
    st.markdown("### Escape Efficiency")
    if not np.isnan(eta_esc):
        st.metric("η_esc", f"{eta_esc:.4f}", help="η_esc = ln(σ)/ln(σa)")
    else:
        st.write("Escape Efficiency: Invalid (check parameters)")
    
    st.divider()
    
    st.markdown("### Additional Parameters")
    st.write(f"**τ:** {tau:.4f}")
    st.write(f"**|ρ|:** {rho_mag:.4f}")
    st.write(f"**φ_a:** {phi_a:.4f} rad ({np.degrees(phi_a):.2f}°)")
    st.write(f"**A_t:** {A_t:.6f}")
    st.write(f"**r_e:** {r_e:.4f}")

# Additional information
with st.expander("Model Information", expanded=False):
    st.markdown("""
    This model implements the **Ring Resonator With Back Reflection** transmission model.
    
    **Key Equations:**
    - Transmission: T_full = (A_t/4) × |numerator/denominator|²
    - Quality Factors: Q = -ω_m/(Δω_FSR) × π/ln(parameter)
    - Escape Efficiency: η_esc = ln(σ)/ln(σa)
    
    **Parameters:**
    - **a**: Ring transmission magnitude (|a_±| = √(τ² + |ρ|²))
    - **σ**: Coupler transmission coefficient
    - **f_delta**: Splitting distance (Δf) between Lorentzian peaks, used to calculate φ_a = π × (f_delta / FSR_ring)
    - **FSR_ring**: Free spectral range of the ring
    - **FSR_fp**: Free spectral range of the Fabry-Pérot cavity
    - **r**: Facet reflectivity
    - **t_fp**: Fabry-Pérot transmission coefficient
    - **δ**: Phase difference (φ_d + φ_e)
    
    For more details, see the documentation in `docs/Ring_Resonator_Model.md`.
    """)

