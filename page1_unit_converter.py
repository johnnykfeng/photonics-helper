import streamlit as st
import tomllib

from equations import (
    dB_to_percent,
    dBm_to_mW,
    frequency_to_wavelength,
    mW_to_dBm,
    omega_to_wavelength,
    percent_to_dB,
    wavelength_to_frequency,
    wavelength_to_omega,
)
from photonic_units import (
    AngularFrequency,
    AngularFrequencyUnit,
    Frequency,
    FrequencyUnit,
    Wavelength,
    WavelengthUnit,
)

st.set_page_config(page_title="Unit Converter", page_icon="🔢", layout="centered")

with open("defaults.toml", "rb") as f:
    defaults = tomllib.load(f)

st.header("Unit Converter")
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("$f \\leftrightarrow \\lambda$")
    freq_input = st.number_input("Input Frequency (GHz)", value=defaults["frequency"], step=0.1)
    frequency = Frequency(value=freq_input, unit=FrequencyUnit.GIGAHERTZ)
    wavelength = frequency_to_wavelength(frequency)
    st.info(f"$\\lambda$ = {wavelength.value:.3f} {wavelength.unit.value}")

    wavelength_input = st.number_input("Input Wavelength (nm)", value=defaults["wavelength"], step=0.1)
    wavelength = Wavelength(value=wavelength_input, unit=WavelengthUnit.NANOMETER)
    frequency = wavelength_to_frequency(wavelength)
    st.info(f"$f$ = {frequency.value:.3f} {frequency.unit.value}")

with col2:
    st.subheader("$\\omega \\leftrightarrow \\lambda$")
    omega_input = st.number_input("Angular Frequency (Trad/s)", value=defaults["omega"], step=0.1)
    omega = AngularFrequency(value=omega_input, unit=AngularFrequencyUnit.TERA_RAD_PER_SEC)
    wavelength = omega_to_wavelength(omega)
    st.info(f"$\\lambda$ = {wavelength.value:.3f} {wavelength.unit.value}")

    wavelength_input2 = st.number_input("Wavelength (nm)", value=defaults["wavelength"], step=0.1, key="wavelength2")
    wavelength = Wavelength(value=wavelength_input2, unit=WavelengthUnit.NANOMETER)
    omega = wavelength_to_omega(wavelength)
    st.info(f"$\\omega$ = {omega.value:.3f} {omega.unit.value}")

st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("$T[dB] \\leftrightarrow T[\\%]$")
    db_input = st.number_input("$T[dB]$", value=0.0, step=0.1)
    percent = dB_to_percent(db_input)
    st.info(f"$T$ = {percent:.3f}%")

    percent_input = st.number_input("$T[\\%]$", value=100.0, step=0.1)
    db = percent_to_dB(percent_input)
    st.info(f"$T[dB]$ = {db:.3f} dB")

with col4:
    st.subheader("$P[mW] \\leftrightarrow P[dBm]$")
    mw_input = st.number_input("Power (mW)", value=1.0, step=0.1)
    dbm = mW_to_dBm(mw_input)
    st.info(f"$P[dBm]$ = {dbm:.3f} dBm")

    dbm_input = st.number_input("Power (dBm)", value=0.0, step=0.1)
    mw = dBm_to_mW(dbm_input)
    st.info(f"$P[mW]$ = {mw:.3f} mW")
