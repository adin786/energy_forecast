import json
import sys

import pandas as pd
import pytest
from loguru import logger

from energy_forecast.app_lambda.app import lambda_handler

# logger.remove()
logger.add(sys.stderr, filter=__name__, level="DEBUG")
JSON_ORIENT = "index"
MODEL_LIST = [
    "naive.zip",
    "naive_seasonal.zip",
    "naive_seasonal_drift.zip",
    "autoarima.zip",
    "sarimax.zip",
    "exp_smoothing.zip",
    # "prophet.zip", # Couldnt get working due to weird datetime related errors
]


def test_handler_hello():
    event = {
        "task": "hello_world",
        "data": "Some data",
    }
    r = lambda_handler(event, None)
    assert isinstance(r, dict)
    assert r["message"] == "Hello world, this is a test function!"


def test_handler_echo():
    some_data = "Some data"
    event = {
        "task": "echo",
        "data": some_data,
    }
    r = lambda_handler(event)
    assert isinstance(r, dict)
    assert r["message"] == some_data


def test_dummy():
    r = lambda_handler({})
    assert isinstance(r, dict)
    assert r["message"] == "Invalid task"


@pytest.mark.parametrize("model_name", MODEL_LIST)
def test_handler_predict_by_periods(model_name):
    # pylint: disable=no-member
    event = {
        "task": "predict_by_periods",
        "data": {"model": model_name, "periods": [1, 2, 3]},
    }
    r = lambda_handler(event)
    assert isinstance(r, dict)
    y_pred = pd.read_json(r["predictions"], orient=JSON_ORIENT)
    assert y_pred.shape == (3, 1)
    assert isinstance(y_pred.index, pd.DatetimeIndex)


@pytest.mark.parametrize("model_name", MODEL_LIST)
def test_handler_predict_by_dates(model_name):
    # pylint: disable=no-member
    dates = pd.PeriodIndex(["2017-02", "2017-03", "2017-04"], freq="M")
    dates = dates.astype(str).to_list()
    event = {
        "task": "predict_by_dates",
        "data": {
            "model": model_name,
            "dates": dates,
        },
    }
    r = lambda_handler(event)
    assert isinstance(r, dict)
    y_pred = pd.read_json(r["predictions"], orient=JSON_ORIENT)
    assert y_pred.shape == (3, 1)
    assert isinstance(y_pred.index, pd.DatetimeIndex)
