import streamlit as st
import tomllib
from equations import (
    linewidth_GHz_to_nm,
    linewidth_nm_to_GHz,
    linewidth_freq_to_wvl,
    linewidth_wvl_to_freq,
)

with open("defaults.toml", "rb") as f:
    defaults = tomllib.load(f)

st.header("Linewidth Converter")


col1, col2 = st.columns(2)

with col1:
    st.subheader("$\\Delta \\lambda\\ = \\frac{\\lambda_0^2}{c} \\Delta \\nu$")
    freq_unit = st.radio("Frequency Unit", ["MHz", "GHz"], index=0, key="freq_unit_1")
    linewidth_freq = st.number_input(f"Linewidth ({freq_unit})", value=defaults["linewidth_MHz"], step=0.1, key="linewidth_freq")
    center_wavelength = st.number_input("Center Wavelength (nm)", value=defaults["wavelength"], step=0.1)

    linewidth_wvl = linewidth_freq_to_wvl(linewidth_freq, center_wavelength, freq_unit)
    st.subheader(f"$\\Delta \\lambda$ = {linewidth_wvl:.6f} nm")


with col2:
    # OLD WAY
    # st.subheader("$\Delta \lambda$ → $\Delta f$")
    # freq_unit = st.radio("Frequency Unit", ["MHz", "GHz"], index=0, key="freq_unit_2")
    # linewidth_nm = st.number_input("Linewidth (nm)", value=defaults["linewidth_nm"], step=0.001, format="%.4f")
    # center_wavelength2 = st.number_input("Center Wavelength (nm)", value=defaults["wavelength"], step=0.1, key="center2")
    # linewidth_ghz = linewidth_nm_to_GHz(linewidth_nm, center_wavelength2)
    # if freq_unit == "GHz":
    #     linewidth_freq = linewidth_ghz
    # else:
    #     linewidth_freq = linewidth_ghz*1e3

    # st.subheader(f"$\Delta f$ = {linewidth_freq:.6f} {freq_unit}")
    # st.divider()

    st.subheader("$\\Delta \\nu\\ = \\frac{c}{\\lambda_0^2} \\Delta \\lambda$")
    freq_unit = st.radio("Frequency Unit", ["MHz", "GHz"], index=0, key="freq_unit_3")
    linewidth_wvl = st.number_input(
        "Linewidth (nm)", 
        value=defaults["linewidth_nm"], 
        step=0.001, 
        format="%.4f", 
        key="linewidth_wvl")
    center_wavelength3 = st.number_input(
        "Center Wavelength (nm)", 
        value=defaults["wavelength"], 
        step=0.1, 
        key="center3")
    linewidth_freq = linewidth_wvl_to_freq(linewidth_wvl, center_wavelength3, freq_unit)
    st.subheader(f"$\\Delta \\nu$ = {linewidth_freq:.6f} {freq_unit}")