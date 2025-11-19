from equations import (frequency_to_wavelength, wavelength_to_frequency, mW_to_dBm, dBm_to_mW)
import streamlit as st
import pandas as pd
import numpy as np

st.header("Tables")
st.divider()

table_choice = st.radio("Select a table", ["Frequency vs Wavelength", "Wavelength vs Frequency", "Power (mW) vs Power (dBm)", "Power (dBm) vs Power (mW)"])
if table_choice == "Frequency vs Wavelength":
    min_value = st.number_input("Min Frequency (GHz)", value=100.0)
    max_value = st.number_input("Max Frequency (GHz)", value=1000.0)
    step_value = st.number_input("Step (GHz)", value=1.0)
    freq_range = np.arange(min_value, max_value, step_value)
    wavelength_range = [frequency_to_wavelength(f) for f in freq_range]
    df = pd.DataFrame({'Frequency (GHz)': freq_range, 'Wavelength (nm)': wavelength_range})
    st.dataframe(df)
elif table_choice == "Wavelength vs Frequency":
    min_value = st.number_input("Min Wavelength (nm)", value=1500.0)
    max_value = st.number_input("Max Wavelength (nm)", value=1600.0)
    step_value = st.number_input("Step (nm)", value=1.0)
    wavelength_range = np.arange(min_value, max_value, step_value)
    freq_range = [wavelength_to_frequency(w) for w in wavelength_range]
    df = pd.DataFrame({'Wavelength (nm)': wavelength_range, 'Frequency (GHz)': freq_range})
    st.dataframe(df)
elif table_choice == "Power (mW) vs Power (dBm)":
    min_value = st.number_input("Min Power (mW)", value=1.0)
    max_value = st.number_input("Max Power (mW)", value=100.0)
    step_value = st.number_input("Step (mW)", value=1.0)
    mW_range = np.arange(min_value, max_value, step_value)
    dBm_range = [mW_to_dBm(mW) for mW in mW_range]
    df = pd.DataFrame({'Power (mW)': mW_range, 'Power (dBm)': dBm_range})
    st.dataframe(df)
elif table_choice == "Power (dBm) vs Power (mW)":
    min_value = st.number_input("Min Power (dBm)", value=0.0)
    max_value = st.number_input("Max Power (dBm)", value=20.0)
    step_value = st.number_input("Step (dBm)", value=1.0)
    dBm_range = np.arange(min_value, max_value, step_value)
    mW_range = [dBm_to_mW(dBm) for dBm in dBm_range]
    df = pd.DataFrame({'Power (dBm)': dBm_range, 'Power (mW)': mW_range})
    st.dataframe(df)