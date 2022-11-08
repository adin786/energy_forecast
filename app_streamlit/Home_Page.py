import streamlit as st
import pandas as pd
import plotly.express as px
import energy_forecast as ef
from energy_forecast.utils import repo_root
from energy_forecast.preprocessing import load_and_set_types
from pathlib import Path

REPO_ROOT = Path(repo_root())
DATA_DIR = REPO_ROOT / "data"


@st.cache
def load_df(path):
    return load_and_set_types(path)


df = load_df(DATA_DIR / "processed" / "train.csv")

st.title("Energy consumption forecasting (UK)")

"""
This app computes timeseries forecasts for
UK monthly energy consumption.

Use the sidebar to switch between this 
interactive forecaster tool, a visual analysis of 
energy trends, and discussion of forecasting model 
results.
"""

# Plot

selected_date = st.date_input("Select a target date for the forecast")

btn_state = st.button('Process')
