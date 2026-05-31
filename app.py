import streamlit as st
import tomllib


unit_converter_page = st.Page("page1_unit_converter.py", title="Unit Converter", icon="🔢")
linewidth_converter_page = st.Page("page2_linewidth_converter.py", title="Linewidth Converter", icon="📏")
plots_page = st.Page("page3_plots.py", title="Plots", icon="📈")
tables_page = st.Page("page4_tables.py", title="Tables", icon="📊")
parquet_loader_page = st.Page("page5_parquet_loader.py", title="Parquet Loader", icon="📋")
ring_resonator_page = st.Page("page6_ring-resonator-model.py", title="Ring Resonator Model", icon="🔄")
pid_lock_page = st.Page("page7_pid_lock.py", title="PID Locking Simulation", icon="🖥️")
about_page = st.Page("about_page.py", title="About", icon="ℹ️")

pg = st.navigation([
    unit_converter_page,
    linewidth_converter_page,
    plots_page,
    tables_page,
    parquet_loader_page,
    ring_resonator_page,
    pid_lock_page,
    about_page])

st.set_page_config(page_title="Photonics Calculator", page_icon="🔬")

pg.run()

