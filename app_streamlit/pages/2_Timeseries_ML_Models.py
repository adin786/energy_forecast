import streamlit as st

"""
# Timeseries Forecasting Models
> *Page in progress*
"""
from pathlib import Path

import streamlit as st

from energy_forecast.utils import repo_root

REPO_ROOT = Path(repo_root())
PLOTS = REPO_ROOT / "assets" / "plots"

"""### Naive (assume last value)
Mean Absolute Percentage Error (MAPE) = 0.379"""
st.image(str(PLOTS / "naive.png"))

"""### Naive seasonal
Mean Absolute Percentage Error (MAPE) = 0.098"""
st.image(str(PLOTS / "naive_seasonal.png"))

"""### Naive with drift
Mean Absolute Percentage Error (MAPE) = 0.321"""
st.image(str(PLOTS / "naive_seasonal_drift.png"))

"""### Auto ARIMA
Mean Absolute Percentage Error (MAPE) = 0.051"""
st.image(str(PLOTS / "autoarima.png"))

"""### SARIMAX
Mean Absolute Percentage Error (MAPE) = 0.055"""
st.image(str(PLOTS / "sarimax.png"))

"""### Exponential Smoothing
Mean Absolute Percentage Error (MAPE) = 0.057"""
st.image(str(PLOTS / "exp_smoothing.png"))

"""
---

## More detail to be added here
...
"""
