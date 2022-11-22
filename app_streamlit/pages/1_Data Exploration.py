from pathlib import Path

import pandas as pd
import streamlit as st

from energy_forecast.preprocessing import load_and_set_types
from energy_forecast.utils import repo_root

REPO_ROOT = Path(repo_root())
DATA_DIR = REPO_ROOT / "data"
TRAIN_CSV = DATA_DIR / "processed" / "train.csv"


@st.cache
def load_df(path):
    return load_and_set_types(path)


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
# Data Exploration
> *Page in progress*
"""

## Display some energy usage data

generate_processed_data()

df = load_df(TRAIN_CSV)
st.write(df)

"""
## More detail to be added here
See notebooks in repo source for latest plots.  These are yet to be integrated into the streamlit app.
- Timeseries plots
- Seasonal plots
- Seasonal subseries plots
- ACF plots
- Residual error plots
- ...


