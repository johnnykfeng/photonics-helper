import streamlit as st
import numpy as np
from equations import frequency_vs_wavelength

def run():
    st.header("Frequency vs Wavelength Plot")
    
    col1, col2 = st.columns(2)
    with col1:
        freq_min = st.number_input("Min Frequency (GHz)", value=100.0)
    with col2:
        freq_max = st.number_input("Max Frequency (GHz)", value=1000.0)
    
    freq_range = np.linspace(freq_min, freq_max, 1000)
    fig = frequency_vs_wavelength(freq_range)
    st.pyplot(fig)