import streamlit as st
import tomllib
from equations import (
    frequency_to_wavelength,
    wavelength_to_frequency,
    omega_to_wavelength,
    wavelength_to_omega,
    dB_to_percent,
    percent_to_dB,
    mW_to_dBm,
    dBm_to_mW,
    # linewidth_GHz_to_nm,
    # linewidth_nm_to_GHz,
    # frequency_vs_wavelength,
    # transmission_plot
)

with open("defaults.toml", "rb") as f:
    defaults = tomllib.load(f)

def run():
    st.header("Unit Converter")
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Frequency ↔ Wavelength")
        freq_input = st.number_input("Input Frequency (GHz)", value=defaults["frequency"], step=0.1)
        wavelength = frequency_to_wavelength(freq_input)
        st.info(f"$\\lambda$ = {wavelength:.3f} nm")
                
        wavelength_input = st.number_input("Input Wavelength (nm)", value=defaults["wavelength"], step=0.1)
        frequency = wavelength_to_frequency(wavelength_input)
        st.info(f"$f$ = {frequency:.3f} GHz")

    with col2:
        st.subheader("Angular Frequency ↔ Wavelength")
        omega_input = st.number_input("Angular Frequency (Trad/s)", value=defaults["omega"], step=0.1)
        wavelength = omega_to_wavelength(omega_input)
        st.info(f"$\\lambda$ = {wavelength:.3f} nm")
        
        wavelength_input2 = st.number_input("Wavelength (nm)", value=defaults["wavelength"], step=0.1, key="wavelength2")
        omega = wavelength_to_omega(wavelength_input2)
        st.info(f"$\\omega$ = {omega:.3f} Trad/s")

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("dB ↔ Percentage")
        db_input = st.number_input("dB", value=0.0, step=0.1)
        percent = dB_to_percent(db_input)
        st.info(f"$T$ = {percent:.3f}%")
        
        percent_input = st.number_input("Percentage (%)", value=100.0, step=0.1)
        db = percent_to_dB(percent_input)
        st.info(f"$T[dB]$ = {db:.3f} dB")

    with col4:
        st.subheader("Power: mW ↔ dBm")
        mw_input = st.number_input("Power (mW)", value=1.0, step=0.1)
        dbm = mW_to_dBm(mw_input)
        st.info(f"$P[dBm]$ = {dbm:.3f} dBm")
        
        dbm_input = st.number_input("Power (dBm)", value=0.0, step=0.1)
        mw = dBm_to_mW(dbm_input)
        st.info(f"$P[mW]$ = {mw:.3f} mW")

