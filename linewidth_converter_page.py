import streamlit as st
import tomllib
from equations import (
    linewidth_GHz_to_nm,
    linewidth_nm_to_GHz
)

with open("defaults.toml", "rb") as f:
    defaults = tomllib.load(f)

def run():
    st.header("Linewidth Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GHz to nm")
        linewidth_ghz = st.number_input("Linewidth (GHz)", value=defaults["linewidth_GHz"], step=0.1)
        center_wavelength = st.number_input("Center Wavelength (nm)", value=defaults["wavelength"], step=0.1)
        linewidth_nm = linewidth_GHz_to_nm(linewidth_ghz, center_wavelength)
        st.subheader(f"{linewidth_nm:.6f} nm")
    
    with col2:
        st.subheader("nm to GHz")
        linewidth_nm = st.number_input("Linewidth (nm)", value=defaults["linewidth_nm"], step=0.001, format="%.4f")
        center_wavelength2 = st.number_input("Center Wavelength (nm)", value=defaults["wavelength"], step=0.1, key="center2")
        linewidth_ghz = linewidth_nm_to_GHz(linewidth_nm, center_wavelength2)
        st.subheader(f"{linewidth_ghz:.6f} GHz")