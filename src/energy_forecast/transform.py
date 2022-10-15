from .loaders import load_ods, load_ods_sheetnames
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def _remove_notes(df: DataFrame) -> DataFrame:
    """Strips out the '[notes]' tag on some column names"""
    df.columns = df.columns.str.replace(r'\[.*\]','', regex=True)
    df.columns = df.columns.str.strip()
    return df


def _remove_average(df: DataFrame) -> DataFrame:
    """Strips out the 'average' suffixon some column names"""
    df.columns = df.columns.str.replace(r'average', '', regex=True)
    return df


def _drop_provisional_rows(df: DataFrame) -> DataFrame:
    """Drops any rows with 'provisional' in the month string"""
    return df[~df.month.str.contains('\[provisional\]')]


def clean_energy_data(df: DataFrame) -> DataFrame:
    """Transforms raw df loaded from gov.uk energy trends .ods file
    into a useful tabular structure, tidies up column names etc.
    If downloaded fresh from the website, the structure of the .ods 
    file has been known to be modified occasionally, in this case 
    you would need to tweak this function."""

    col_renamer = {
        'primary electricity - net imports': 'elec_import',
        'primary electricity - wind, solar and hydro': 'elec_renewable',
        'primary electricity - nuclear': 'elec_nuclear'
    }

    # Run a sequence of chained pandas methods to clean the raw input
    df = (df
        .set_axis(df.iloc[3, :].tolist(),
                  axis=1)
        .rename(columns=str.lower)
        .iloc[4:]
        .pipe(_drop_provisional_rows)
        .reset_index(drop=True)
        .pipe(_remove_notes)
        .iloc[:,:9]
        .rename(columns=col_renamer)
        .assign(month=lambda x: pd.to_datetime(x.month))
        .rename(columns={'month': 'datetime'})
        .set_index('datetime')
        .replace('[x]', np.nan)
        .astype(float)
    )
    return df


def clean_temp_data(df: DataFrame) -> DataFrame:
    """Transforms/cleans raw temperature data into dataframe"""
    df = (df
        .set_axis(df.iloc[3, :].tolist(),
            axis=1)
        .iloc[4:16]
        .rename(columns=str.lower)
        .rename(columns={'calendar period': 'month'})
        .pipe(_remove_notes)
        .pipe(_remove_average)
        .drop(columns=['30-year mean'])
        .replace('[x]', np.nan)
        .melt(id_vars='month', var_name='year', value_name='temp')
        .assign(datetime=lambda x: x.month + ' ' + x.year)
        .assign(datetime=lambda x: pd.to_datetime(x.datetime))
        .drop(columns=['month', 'year'])
        .set_index('datetime')
    )
    return df


def clean_wind_data(df: DataFrame) -> DataFrame:
    """Transforms/cleans raw wind data into dataframe"""
    df = (df
        .set_axis(df.iloc[3, :].tolist(),
            axis=1)
        .iloc[4:16]
        .rename(columns=str.lower)
        .rename(columns={'calendar period': 'month'})
        .pipe(_remove_notes)
        .pipe(_remove_average)
        .drop(columns=['20-year mean'])
        .replace('[x]', np.nan)
        .melt(id_vars='month', var_name='year', value_name='wind')
        .assign(datetime=lambda x: x.month + ' ' + x.year)
        .assign(datetime=lambda x: pd.to_datetime(x.datetime))
        .drop(columns=['month', 'year'])
        .set_index('datetime')
    )
    return df


def clean_sun_data(df: DataFrame) -> DataFrame:
    """Transforms/cleans raw sunlight data into dataframe"""
    df = (df
        .set_axis(df.iloc[3, :].tolist(),
            axis=1)
        .iloc[4:16]
        .rename(columns=str.lower)
        .rename(columns={'calendar period': 'month'})
        .pipe(_remove_notes)
        .pipe(_remove_average)
        .drop(columns=['20-year mean'])
        .replace('[x]', np.nan)
        .melt(id_vars='month', var_name='year', value_name='sun')
        .assign(datetime=lambda x: x.month + ' ' + x.year)
        .assign(datetime=lambda x: pd.to_datetime(x.datetime))
        .drop(columns=['month', 'year'])
        .set_index('datetime')
    )
    return df


def clean_rain_data(df: DataFrame) -> DataFrame:
    """Transforms/cleans raw rainfall data into dataframe"""
    df = (df
        .set_axis(df.iloc[3, :].tolist(),
            axis=1)
        .iloc[4:16]
        .rename(columns=str.lower)
        .rename(columns={'calendar period': 'month'})
        .pipe(_remove_notes)
        .pipe(_remove_average)
        .drop(columns=['20-year mean'])
        .replace('[x]', np.nan)
        .melt(id_vars='month', var_name='year', value_name='rain')
        .assign(datetime=lambda x: x.month + ' ' + x.year)
        .assign(datetime=lambda x: pd.to_datetime(x.datetime))
        .drop(columns=['month', 'year'])
        .set_index('datetime')
    )
    return df

