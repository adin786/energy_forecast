import pandas as pd
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, filter=__name__, level="INFO")

TARGET_COL = "total_energy"
EXPLANATORY_COLS = ["temp", "wind", "sun", "rain"]


def load_and_set_types(path: str) -> pd.DataFrame:
    """Load csv and set types"""
    logger.debug("Loading csv and setting types")
    df = (
        pd.read_csv(path)
        .assign(datetime=lambda x: pd.to_datetime(x["datetime"], format="%Y-%m-%d"))
        .set_index("datetime", drop=True)
    )
    return df


def crop(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Trim the data between two dates"""
    logger.debug(f"Trimming between {start} and {end}")
    df = df.loc[start:end]
    return df


def add_year_month(df: pd.DataFrame) -> pd.DataFrame:
    """Add year and month cols for seasonal plotting"""
    df = df.assign(
        year=lambda x: x.index.to_series().dt.year,
        month=lambda x: x.index.to_series().dt.month,
    )
    return df


def prepare_y(df: pd.DataFrame) -> pd.DataFrame:
    """Extract target variable and add features"""
    y_train = df.loc[:, [TARGET_COL]].pipe(add_year_month)
    return y_train


def prepare_x(df: pd.DataFrame) -> pd.DataFrame:
    """Extract explanatory variables and add features"""
    x_train = df.loc[:, EXPLANATORY_COLS].pipe(add_year_month)
    return x_train


def load_and_prepare_y(path: str) -> pd.DataFrame:
    """One line to load and prepare target variable y"""
    df = load_and_set_types(path).loc[:, [TARGET_COL]].to_period("M")
    return df


def load_and_prepare_x(path: str) -> pd.DataFrame:
    """One line to load and prepare explanatory variables x"""
    df = load_and_set_types(path).loc[:, EXPLANATORY_COLS].to_period("M")
    return df
