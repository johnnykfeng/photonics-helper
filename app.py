import streamlit as st
import tomllib


unit_converter_page = st.Page("unit_converter_page.py", title="Unit Converter", icon="🔢")
linewidth_converter_page = st.Page("linewidth_converter_page.py", title="Linewidth Converter", icon="📏")
plots_page = st.Page("plots_page.py", title="Plots", icon="📈")
about_page = st.Page("about_page.py", title="About", icon="ℹ️")
pg = st.navigation([
    unit_converter_page, 
    linewidth_converter_page, 
    plots_page, 
    about_page])
st.set_page_config(page_title="Photonics Helper", page_icon="🔬", layout="centered")
pg.run()

# # Constants
# c = 2.998e8  # Speed of light in m/s

# # Main app
# st.title("🔬 Photonics Helper")
# st.markdown("A comprehensive tool for photonics calculations and visualizations")

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Choose a tool:", [
#     "Unit Converter",
#     "Linewidth Converter", 
#     "Frequency-Wavelength Plot",
#     # "Transmission Plot",
#     "About"
# ])

# if page == "Unit Converter":
#     import unit_converter_page
#     unit_converter_page.run()

# elif page == "Linewidth Converter":
#     import linewidth_converter_page
#     linewidth_converter_page.run()

# elif page == "Frequency-Wavelength Plot":
#     import plots_page
#     plots_page.run()

# elif page == "About":
#     st.header("About Photonics Helper")
#     st.markdown("""
#     This Streamlit app provides common photonics calculations and visualizations.
    
#     ### Default Units:
#     - **Wavelength**: nm (nanometers) or 1e-9 m
#     - **Angular Frequency (ω)**: Trad/s (tera-radians per second) or 1e12 rad/s
#     - **Frequency (f)**: GHz (gigahertz) or 1e9 Hz
#     - **Quality Factor (Q)**: M (millions)
#     - **Transmission/Loss**: dB (decibels)
#     - **Power**: mW (milliwatts) or dBm
    
#     ### Features:
#     - Unit conversions between frequency, wavelength, and angular frequency
#     - Power conversions between mW and dBm
#     - Transmission conversions between dB and percentage
#     - Linewidth conversions between GHz and nm
#     - Interactive plotting tools for frequency-wavelength relationships
#     - Sample transmission plots
    
#     ### Physics Constants:
#     - Speed of light: c = 2.998 × 10⁸ m/s
#     """)

