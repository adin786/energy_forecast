import streamlit as st
import pandas as pd
import plotly.express as px
import energy_forecast as ef
from energy_forecast.utils import repo_root
from energy_forecast.preprocessing import load_and_set_types
from energy_forecast.deploy.aws_lambda import invoke_lambda_function
from pathlib import Path

REPO_ROOT = Path(repo_root())
DATA_DIR = REPO_ROOT / "data"
TRAIN_CSV = DATA_DIR / "processed" / "train.csv"


@st.cache
def load_df(path):
    return load_and_set_types(path)

@st.cache
def get_inference_response(input_date):
    return invoke_lambda_function('energy_forecast', payload={'input_date': str(input_date)})

def generate_processed_data():
    if not TRAIN_CSV.exists():
        from dvc.api import DVCFileSystem
        import time
        url = "https://github.com/adin786/energy_forecast.git"
        fs = DVCFileSystem(".")
        with fs.open("data/processed/train.csv") as f, st.spinner('Syncing datafile using DVC[S3]'):
            df = pd.read_csv(f, index_col=0)
            TRAIN_CSV.parent.mkdir(parents=True)
            df.to_csv(TRAIN_CSV)
            time.sleep(3)

st.title("Energy consumption forecasting (UK)")

"""
This app computes timeseries forecasts for
UK monthly energy consumption.

Use the sidebar to switch between this 
interactive forecaster tool, a visual analysis of 
energy trends data, and discussion of forecasting model 
results.
"""

"""
## Request a model prediction from the inference API

The model is deployed as a serverless lambda function and we can query it 
for a result using `boto3` pre-configured with AWS credentials
"""

selected_date = st.date_input("Select a target date for the forecast")

btn_state = st.button("Process")

if btn_state:
    response = get_inference_response(selected_date)
    st.write('The inference "server" responded with:')
    st.write(response)
    st.write('Try picking a different date further in the future and re-process')


"""
---
## Display some energy usage data
"""
generate_processed_data()

df = load_df(TRAIN_CSV)
st.write(df)
