# Here's the plotting functions

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def frequency_vs_wavelength(freq_range_ghz=None, wavelength_range_nm=None):
    """Plot frequency vs wavelength relationship"""
    if freq_range_ghz is None:
        freq_range_ghz = np.linspace(100, 1000, 1000)  # 100-1000 GHz
    wavelengths = [frequency_to_wavelength(f) for f in freq_range_ghz]
    return wavelengths