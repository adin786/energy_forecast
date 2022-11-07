import pandas as pd
import warnings
from pathlib import Path


def load_ods(path: str, sheet_name: str) -> pd.DataFrame:
    """Loads an ods file to a dataframe"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            engine="odf",
        )
    return df


def load_ods_sheetnames(path: str) -> list:
    """Loads an ods file's sheetnames"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sheets = pd.read_excel(
            path,
            sheet_name=None,
            engine="odf",
        )
    return list(sheets.keys())
