import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

c = 2.998e8  # Speed of light in m/s

# Conversion functions
def frequency_to_wavelength(freq_ghz):
    """Convert frequency in GHz to wavelength in nm"""
    freq_hz = freq_ghz * 1e9
    wavelength_m = c / freq_hz
    wavelength_nm = wavelength_m * 1e9
    return wavelength_nm

def wavelength_to_frequency(wavelength_nm):
    """Convert wavelength in nm to frequency in GHz"""
    wavelength_m = wavelength_nm * 1e-9
    freq_hz = c / wavelength_m
    freq_ghz = freq_hz / 1e9
    return freq_ghz

def omega_to_wavelength(omega_trad_s):
    """Convert angular frequency in Trad/s to wavelength in nm"""
    omega_rad_s = omega_trad_s * 1e12
    wavelength_m = 2 * np.pi * c / omega_rad_s
    wavelength_nm = wavelength_m * 1e9
    return wavelength_nm

def wavelength_to_omega(wavelength_nm):
    """Convert wavelength in nm to angular frequency in Trad/s"""
    wavelength_m = wavelength_nm * 1e-9
    omega_rad_s = 2 * np.pi * c / wavelength_m
    omega_trad_s = omega_rad_s / 1e12
    return omega_trad_s

def dB_to_percent(dB):
    """Convert dB to percentage"""
    return 100 * (10**(dB/10))

def percent_to_dB(percent):
    """Convert percentage to dB"""
    return 10 * np.log10(percent/100)

def mW_to_dBm(mW):
    """Convert mW to dBm"""
    return 10 * np.log10(mW)

def dBm_to_mW(dBm):
    """Convert dBm to mW"""
    return 10**(dBm/10)

def linewidth_GHz_to_nm(linewidth_ghz, center_wavelength_nm):
    """Convert linewidth from GHz to nm"""
    center_freq_ghz = wavelength_to_frequency(center_wavelength_nm)
    wavelength_nm = frequency_to_wavelength(center_freq_ghz + linewidth_ghz/2)
    wavelength_nm2 = frequency_to_wavelength(center_freq_ghz - linewidth_ghz/2)
    return abs(wavelength_nm - wavelength_nm2)

def linewidth_nm_to_GHz(linewidth_nm, center_wavelength_nm):
    """Convert linewidth from nm to GHz"""
    freq1_ghz = wavelength_to_frequency(center_wavelength_nm + linewidth_nm/2)
    freq2_ghz = wavelength_to_frequency(center_wavelength_nm - linewidth_nm/2)
    return abs(freq1_ghz - freq2_ghz)

# Plotting functions
def frequency_vs_wavelength(freq_range_ghz=None, wavelength_range_nm=None):
    """Plot frequency vs wavelength relationship"""
    if freq_range_ghz is None:
        freq_range_ghz = np.linspace(100, 1000, 1000)  # 100-1000 GHz
    
    wavelengths = [frequency_to_wavelength(f) for f in freq_range_ghz]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(freq_range_ghz, wavelengths, 'b-', linewidth=2)
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Wavelength (nm)')
    ax.set_title('Frequency vs Wavelength')
    ax.grid(True, alpha=0.3)
    
    return fig

def frequency_vs_wavelength_plotly(freq_range_ghz=None, wavelength_range_nm=None):
    """Plot frequency vs wavelength relationship"""
    if freq_range_ghz is None:
        freq_range_ghz = np.linspace(100, 1000, 1000)  # 100-1000 GHz
    
    wavelengths = [frequency_to_wavelength(f) for f in freq_range_ghz]
    
    return wavelengths

def transmission_plot(frequencies, transmission_dB):
    """Plot transmission vs frequency"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frequencies, transmission_dB, 'r-', linewidth=2)
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Transmission (dB)')
    ax.set_title('Transmission vs Frequency')
    ax.grid(True, alpha=0.3)
    
    return fig
