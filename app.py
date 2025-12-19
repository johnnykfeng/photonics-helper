import streamlit as st
import tomllib


unit_converter_page = st.Page("page1_unit_converter.py", title="Unit Converter", icon="🔢")
linewidth_converter_page = st.Page("page2_linewidth_converter.py", title="Linewidth Converter", icon="📏")
plots_page = st.Page("page3_plots.py", title="Plots", icon="📈")
tables_page = st.Page("page4_tables.py", title="Tables", icon="📊")
parquet_loader_page = st.Page("page5_parquet_loader.py", title="Parquet Loader", icon="📋")
about_page = st.Page("about_page.py", title="About", icon="ℹ️")
pg = st.navigation([
    unit_converter_page, 
    linewidth_converter_page, 
    plots_page, 
    tables_page,
    parquet_loader_page,
    about_page])
st.set_page_config(page_title="Photonics Calculator", page_icon="🔬", layout="centered")
pg.run()

