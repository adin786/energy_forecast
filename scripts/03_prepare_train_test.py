from energy_forecast.utils import repo_root
from energy_forecast.preprocessing import load_and_set_types, crop
from sktime.forecasting.model_selection import temporal_train_test_split
from pathlib import Path
import click
import pandas as pd
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")


REPO_ROOT = Path(repo_root())
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_INTERIM = REPO_ROOT / "data" / "interim"
DATA_FILE_PATH = DATA_INTERIM / "transformed_energy_weather.csv"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"


@click.command()
def main():
    logger.info("Starting prepare train_test script")
    df = load_and_set_types(DATA_FILE_PATH)

    weather_cols = {
        "temp": "degC",
        "wind": "knots",
        "sun": "hours",
        "rain": "mm",
    }
    energy_cols = {
        "total_energy": "mtoe",
        "coal": "mtoe",
        "petroleum": "mtoe",
        "natural gas": "mtoe",
        "bioenergy & waste": "mtoe",
        "elec_nuclear": "mtoe",
        "elec_renewable": "mtoe",
        "elec_import": "mtoe",
    }
    combined_cols = dict(**energy_cols, **weather_cols)

    df = crop(df, start="2001-01-01", end="2022-06-01")
    logger.debug(f"Shape of overall df after crop: {df.shape}")

    splits = temporal_train_test_split(
        df[["total_energy"]], df[weather_cols.keys()], test_size=0.25
    )
    y_train, y_test, x_train, x_test = splits
    logger.debug(f"Shape of resulting splits: {[a.shape for a in splits]}")

    logger.info("Saving to disk")
    y_train.to_csv(DATA_PROCESSED / "y_train.csv")
    y_test.to_csv(DATA_PROCESSED / "y_test.csv")
    x_train.to_csv(DATA_PROCESSED / "x_train.csv")
    x_test.to_csv(DATA_PROCESSED / "x_test.csv")

    logger.info("Done")


if __name__ == "__main__":
    main()
