import pandas as pd
from pandas import DataFrame
from loguru import logger
import sys
logger.remove()
logger.add(sys.stderr, level='INFO')


def load_and_set_types(path: str) -> DataFrame:
    """Load csv and set types"""
    logger.debug('Loading csv and setting types')
    df = (
        pd.read_csv(path)
        .assign(datetime=lambda x: pd.to_datetime(x['datetime'], format='%Y-%m-%d'))
        .set_index('datetime', drop=True)
    )
    return df


def crop(df: DataFrame, start: str, end: str) -> DataFrame:
    """Trim the data between two dates"""
    logger.debug(f'Trimming between {start} and {end}')
    df = df.loc[start:end]
    return df