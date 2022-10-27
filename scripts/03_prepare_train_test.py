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

    df = crop(df, start="2001-01-01", end="2022-06-01")
    logger.debug(f"Shape of overall df after crop: {df.shape}")

    train, test = temporal_train_test_split(df, test_size=0.25)
    logger.debug(f"Shape of resulting splits: {[a.shape for a in [train, test]]}")
    logger.info("Temporal split complete")

    logger.info("Saving to disk")
    train.to_csv(DATA_PROCESSED / "train.csv")
    test.to_csv(DATA_PROCESSED / "test.csv")

    logger.info("Done")


if __name__ == "__main__":
    main()
