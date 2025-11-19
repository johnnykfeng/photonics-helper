import streamlit as st
import numpy as np
from plots import (
    frequency_vs_wavelength_plot, 
    wavelength_vs_frequency_plot, 
    mW_vs_dBm_plot, 
    dBm_vs_mW_plot
    )
with st.expander("mW vs dBm", expanded=True):

    col1, col2 = st.columns(2)
    with col1:
        mW_min = st.number_input("Min mW", value=1.0)
    with col2:
        mW_max = st.number_input("Max mW", value=100.0)

    mW_range = np.linspace(mW_min, mW_max, 1000)
    fig = mW_vs_dBm_plot(mW_range)
    st.plotly_chart(fig)

with st.expander("dBm vs mW", expanded=True):

    col1, col2 = st.columns(2)
    with col1:
        dBm_min = st.number_input("Min dBm", value=0.0)
    with col2:
        dBm_max = st.number_input("Max dBm", value=20.0)

    dBm_range = np.linspace(dBm_min, dBm_max, 1000)
    fig = dBm_vs_mW_plot(dBm_range)
    st.plotly_chart(fig)

with st.expander("Wavelength vs Frequency", expanded=True):

    col1, col2 = st.columns(2)
    with col1:
        wavelength_min = st.number_input("Min Wavelength (nm)", value=1500.0)
    with col2:
        wavelength_max = st.number_input("Max Wavelength (nm)", value=1600.0)

    wavelength_range = np.linspace(wavelength_min, wavelength_max, 1000)
    fig = wavelength_vs_frequency_plot(wavelength_range)
    st.plotly_chart(fig)

with st.expander("Frequency vs Wavelength", expanded=True):

    col1, col2 = st.columns(2)
    with col1:
        freq_min = st.number_input("Min Frequency (GHz)", value=1e5)
    with col2:
        freq_max = st.number_input("Max Frequency (GHz)", value=5e5)

    freq_range = np.linspace(freq_min, freq_max, 1000)
    fig = frequency_vs_wavelength_plot(freq_range)
    st.plotly_chart(fig)

