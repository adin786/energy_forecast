"""Placeholder"""
from pathlib import Path
import pandas as pd
from energy_forecast.loaders import load_ods, load_ods_sheetnames
import pytest

TEST_FILE = Path(__file__).parent / "test_ods.ods"


@pytest.fixture
def sheet_names():
    return load_ods_sheetnames(TEST_FILE)


def test_load_ods(sheet_names):
    sheet_1 = load_ods(TEST_FILE, sheet_names[0])
    assert isinstance(sheet_1, pd.DataFrame)
    assert sheet_1.shape == (0, 2)
    assert sheet_1.columns[0] == "Cell A1"
    assert sheet_1.columns[1] == "Cell A2"


def test_load_ods_sheetnames(sheet_names):
    assert isinstance(sheet_names, list)
    assert sheet_names == ["Sheet1", "Sheet2"]
