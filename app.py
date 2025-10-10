import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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
    linewidth_GHz_to_nm,
    linewidth_nm_to_GHz,
    frequency_vs_wavelength,
    transmission_plot
)
# Page configuration
st.set_page_config(
    page_title="Photonics Helper",
    page_icon="🔬",
    layout="centered"
)

with open("defaults.toml", "rb") as f:
    defaults = tomllib.load(f)

# Constants
c = 2.998e8  # Speed of light in m/s

# Main app
st.title("🔬 Photonics Helper")
st.markdown("A comprehensive tool for photonics calculations and visualizations")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a tool:", [
    "Unit Converter",
    "Linewidth Converter", 
    "Frequency-Wavelength Plot",
    # "Transmission Plot",
    "About"
])

if page == "Unit Converter":
    import unit_converter_page
    unit_converter_page.run()

elif page == "Linewidth Converter":
    import linewidth_converter_page
    linewidth_converter_page.run()

elif page == "Frequency-Wavelength Plot":
    import plots_page
    plots_page.run()

# elif page == "Transmission Plot":
#     st.header("Transmission Plot")
    
#     st.subheader("Generate Sample Data")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         center_freq = st.number_input("Center Frequency (GHz)", value=300.0)
#     with col2:
#         bandwidth = st.number_input("Bandwidth (GHz)", value=50.0)
#     with col3:
#         max_transmission = st.number_input("Max Transmission (dB)", value=0.0)
    
#     if st.button("Generate Transmission Plot"):
#         frequencies = np.linspace(center_freq - bandwidth/2, center_freq + bandwidth/2, 1000)
#         # Simple Gaussian-like transmission curve
#         transmission = max_transmission - 3 * ((frequencies - center_freq) / (bandwidth/4))**2
#         transmission = np.maximum(transmission, -60)  # Limit minimum transmission
        
#         fig = transmission_plot(frequencies, transmission)
#         st.pyplot(fig)

elif page == "About":
    st.header("About Photonics Helper")
    st.markdown("""
    This Streamlit app provides common photonics calculations and visualizations.
    
    ### Default Units:
    - **Wavelength**: nm (nanometers) or 1e-9 m
    - **Angular Frequency (ω)**: Trad/s (tera-radians per second) or 1e12 rad/s
    - **Frequency (f)**: GHz (gigahertz) or 1e9 Hz
    - **Quality Factor (Q)**: M (millions)
    - **Transmission/Loss**: dB (decibels)
    - **Power**: mW (milliwatts) or dBm
    
    ### Features:
    - Unit conversions between frequency, wavelength, and angular frequency
    - Power conversions between mW and dBm
    - Transmission conversions between dB and percentage
    - Linewidth conversions between GHz and nm
    - Interactive plotting tools for frequency-wavelength relationships
    - Sample transmission plots
    
    ### Physics Constants:
    - Speed of light: c = 2.998 × 10⁸ m/s
    """)

