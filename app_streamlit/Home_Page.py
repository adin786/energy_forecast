import json
import time
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dvc.api import DVCFileSystem

import energy_forecast as ef
from energy_forecast.deploy.aws_lambda import invoke_lambda_function
from energy_forecast.preprocessing import load_and_set_types
from energy_forecast.utils import repo_root

REPO_ROOT = Path(repo_root())
DATA_DIR = REPO_ROOT / "data"
TRAIN_CSV = DATA_DIR / "processed" / "train.csv"
TEST_CSV = DATA_DIR / "processed" / "test.csv"
MODELS = {
    "Naive": "naive.zip",
    "Naive seasonal": "naive_seasonal.zip",
    "Naive with drift": "naive_seasonal_drift.zip",
    "AutoARIMA": "autoarima.zip",
    "SARIMAX": "sarimax.zip",
    "Exponential smoothing": "exp_smoothing.zip",
}


@st.cache
def load_df(path):
    return load_and_set_types(path)


def date_range_to_list(end_date, start_date="2017-02"):
    datetimes = pd.date_range("2017-02", selected_date, freq="M")
    return pd.PeriodIndex(datetimes).to_series().astype(str).to_list()


# @st.cache
def get_predict_by_dates(dates, model_name):
    event = {
        "task": "predict_by_dates",
        "data": {
            "model": model_name,
            "dates": dates,
        },
    }
    response = invoke_lambda_function(
        "energy_forecast",
        payload=event,
    )
    return response


@st.cache
def gather_data_files():
    fs = DVCFileSystem(".")
    with st.spinner("Syncing datafile using DVC[S3]"):
        relative_train = TRAIN_CSV.relative_to(Path.cwd())
        with fs.open(relative_train) as f:
            train = pd.read_csv(f, index_col=0)
        relative_test = TEST_CSV.relative_to(Path.cwd())
        with fs.open(relative_test) as f:
            test = pd.read_csv(f, index_col=0)
    time.sleep(2)
    return train, test


def generate_processed_data():
    if not TRAIN_CSV.exists():
        import time

        from dvc.api import DVCFileSystem

        fs = DVCFileSystem(".")
        with fs.open("data/processed/train.csv") as f, st.spinner(
            "Syncing datafile using DVC[S3]"
        ):
            df = pd.read_csv(f, index_col=0)
            TRAIN_CSV.parent.mkdir(parents=True)
            df.to_csv(TRAIN_CSV)
            time.sleep(3)


"""
# Energy consumption forecasting (UK)
This app computes timeseries forecasts for
UK monthly energy consumption.

Use the sidebar to switch between this 
interactive forecaster tool, a visual analysis of 
energy trends data, and discussion of forecasting model 
results.
"""

# Gather files
train, test = gather_data_files()

# Plot
# "May remove this plot later"
# plot_container = st.empty()
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=train.index, y=train["total_energy"], name="Train"))
# fig.add_trace(go.Scatter(x=test.index, y=test["total_energy"], name="Test"))
# plot_container.plotly_chart(fig)


"""
## Generate a forecast
Select a model to run, and the end-date for the forecast.
All dates are rounded to their nearest month
"""

col1, col2 = st.columns(2)
with col1:
    selected_model = st.selectbox("Select a forecasting model to run", MODELS.keys())

with col2:
    selected_date = st.date_input(
        "Select a target date for the forecast",
        value=date(2022, 6, 30),
        max_value=date(2030, 1, 1),
    )

btn_state = st.button("Process")

selected_model_name = MODELS[selected_model]
dates = date_range_to_list(selected_date)
st.write(f"Forecast will be computed between: {dates[0]} and {dates[-1]}")

# Plot
plot_container2 = st.empty()
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=train.index,
        y=train["total_energy"],
        name="Train",
        line=dict(color="royalblue"),
    )
)
fig.add_trace(
    go.Scatter(
        x=test.index, y=test["total_energy"], name="Test", line=dict(color="indianred")
    )
)
fig.update_layout(
    title="Total UK Energy consumption",
    xaxis_title="Date",
    yaxis_title="Mtoe (Million Tons Oil equiv.)",
)
plot_container2.plotly_chart(fig)


if btn_state:
    response = get_predict_by_dates(dates, selected_model_name)

    if not "predictions" in response:
        st.error(
            'The response did not contain the "predictions" or "orient" keys.\n'
            "Try processing again."
        )
        print(response)
    else:
        predictions = json.loads(response["predictions"])
        preds = pd.DataFrame.from_dict(predictions, orient=response["orient"])
        preds = preds.assign(date=preds.index)

        fig.add_trace(
            go.Scatter(
                x=preds.index,
                y=preds["total_energy"],
                name="Forecast",
                line=dict(color="royalblue", dash="dot"),
            )
        )
        fig.update_layout(
            title="Total UK Energy consumption - with forecast",
            xaxis_title="Date",
            yaxis_title="Mtoe (Million Tons Oil equiv.)",
        )
        plot_container2.plotly_chart(fig)


"""
---

# How Does it Work
- `Jupyter` notebooks and python scripts for experimentation and model building
    - We track our experiments to `Mlflow`, local tracking server
    - Using custom wrapper class to interface `Mlflow` with `sktime` estimator
- Data files and model artifacts are tracked with `DVC`, synced to remote `S3` storage
- `Github actions` for **Continuous Deployment** on merge to Main
    - Build `Docker` image for `Lambda function`
        - Multi-stage build keeps image size <300Mb
        - Model artifacts are baked into `Docker` image (see todo list)
        - Image is pushed to `ECR`
    - Run `Terraform` scripts to spin up cloud infrastructure
        - `Lambda function`
        - `IAM` roles
        - `Cloudwatch` for monitoring
- `Lambda` function acts as **serverless abstraction** for all inference requests
    - Model predictions requested through `boto3` lambda invocation
    - Authentication to `Lambda` requires `IAM` credentials
    - Logs activity to `Cloudwatch` for monitoring usage
- This `Streamlit` app provides an interactive way
    - Uses `DVC` to access versioned data files for plotting etc
    - `Lambda` communication logic abstracted away in custom `energy_forecast` package
"""
