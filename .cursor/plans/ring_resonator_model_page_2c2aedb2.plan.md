---
name: Ring Resonator Model Page
overview: Create a Streamlit page that implements the T_full transmission model from the ring resonator documentation, with interactive sliders for all model parameters and displays calculated quality factors and escape efficiency.
todos:
  - id: create_page_file
    content: Create page6_ring-resonator-model.py with Streamlit page structure and imports
    status: pending
  - id: implement_sliders
    content: Implement all parameter sliders with reasonable defaults and ranges
    status: pending
    dependencies:
      - create_page_file
  - id: implement_t_full
    content: Implement T_full calculation function with all intermediate parameter calculations
    status: pending
    dependencies:
      - create_page_file
  - id: implement_plotting
    content: Create Plotly visualization for T_full vs f_delta
    status: pending
    dependencies:
      - implement_t_full
  - id: implement_metrics
    content: Calculate and display quality factors and escape efficiency
    status: pending
    dependencies:
      - create_page_file
  - id: integrate_app
    content: Add ring resonator page to app.py navigation
    status: pending
    dependencies:
      - create_page_file
---

# Ring Resonator Model Implementation Plan

## Overview

Create `page6_ring-resonator-model.py` that implements the T_full transmission model with interactive parameter controls and displays derived metrics.

## Implementation Details

### 1. Page Structure

- Create Streamlit page following the pattern of other pages (e.g., `page5_parquet_loader.py`)
- Use Plotly for interactive plots (consistent with `plots.py`)
- Organize UI with columns for sliders and plots

### 2. Parameter Sliders

Implement sliders for the following parameters with reasonable physics-based defaults:

- **a**: Ring transmission magnitude (0.8-1.0, default ~0.95)
- **sigma**: Coupler transmission coefficient (0.5-1.0, default ~0.9)
- **f_delta**: Frequency offset range for plotting (e.g., -5 to 5 GHz, default range)
- **f_FSRring**: Ring free spectral range (1-100 GHz, default ~10 GHz)
- **f_FSRfp**: Fabry-Pérot free spectral range (1-100 GHz, default ~10 GHz)
- **r**: Facet reflectivity (0.0-0.5, default ~0.1)
- **t_fp**: Fabry-Pérot transmission coefficient (0.5-1.0, default ~0.9)
- **delta**: Phase difference (0-2π, default ~0)
- **IL_t**: Transmission insertion loss (0.5-1.0, default 1.0)
- **IL_r**: Reflection insertion loss (0.5-1.0, default 1.0)

### 3. T_full Calculation

Implement the simplified T_full equation from [docs/Ring_Resonator_Model.md](docs/Ring_Resonator_Model.md) (line 57):

- Calculate intermediate parameters:
- `phi_a = pi * (f_delta / FSR_ring)` (from user's clarification)
- `tau = a * cos(phi_a)`
- `|rho| = a * sin(phi_a)` (assuming phi_e = 0, so rho is real)
- `a_± = a * e^(±i*phi_a) * e^(i*phi_r)` where `phi_r = 2*pi * (f_delta / FSR_ring)`
- `phi_fp = pi * (f_delta / FSR_fp)`
- `A_t = IL_t * (1-r^2)^2 * t_fp^4`
- `r_e = r * t_fp^2`
- Use numpy for complex number arithmetic
- Calculate T_full for a range of f_delta values

### 4. Plotting

- Create Plotly figure with T_full vs f_delta
- Use `plotly.graph_objects` (consistent with `plots.py`)
- Add proper axis labels and hover information
- Display in Streamlit using `st.plotly_chart()`

### 5. Derived Metrics Display

Calculate and display (from [docs/Ring_Resonator_Model.md](docs/Ring_Resonator_Model.md) section 3):

- **Quality Factors** (using default resonance frequency ~193 THz):
- Loaded Q: `Q_load = -omega_m / Delta_omega_FSR * pi / ln(sigma*a)`
- Extrinsic Q: `Q_ext = -omega_m / Delta_omega_FSR * pi / ln(sigma)`
- Intrinsic Q: `Q_int = -omega_m / Delta_omega_FSR * pi / ln(a)`
- Where `Delta_omega_FSR = 2*pi*FSR_ring`
- **Escape Efficiency**: `eta_esc = ln(sigma) / ln(sigma*a)`
- Display metrics in formatted columns or expandable sections

### 6. Integration

- Add the new page to `app.py` navigation:
  ```python
        ring_resonator_page = st.Page("page6_ring-resonator-model.py", title="Ring Resonator Model", icon="🔄")
  ```




## Files to Modify

- **Create**: `page6_ring-resonator-model.py` - Main implementation
- **Modify**: `app.py` - Add page to navigation

## Technical Notes

- Use numpy for all mathematical operations