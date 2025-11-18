import streamlit as st

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