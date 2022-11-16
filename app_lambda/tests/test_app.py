import pytest
import json
from ..app import lambda_handler
import pandas as pd
from loguru import logger
import sys

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
    response = lambda_handler(event, {})
    logger.debug(f"{response=}")
    r = json.loads(response)
    logger.debug(f"{r=}")
    assert isinstance(response, str)
    assert isinstance(r, dict)
    assert "message" in r
    assert r["message"] == "Hello world, this is a test function!"


def test_handler_echo():
    some_data = "Some data"
    event = {
        "task": "echo",
        "data": some_data,
    }
    response = lambda_handler(event, {})
    logger.debug(f"{response=}")
    r = json.loads(response)
    logger.debug(f"{r=}")
    assert isinstance(response, str)
    assert isinstance(r, dict)
    assert "message" in r
    assert r["message"] == some_data


def test_dummy():
    response = lambda_handler({}, {})
    r = json.loads(response)
    assert isinstance(response, str)
    assert isinstance(r, dict)
    assert "message" in r
    assert r["message"] == "Invalid task"

@pytest.mark.parametrize(
    "model_name", 
    MODEL_LIST
)
def test_handler_predict_by_periods(model_name):
    event = {
        "task": "predict_by_periods",
        "data": {
            "model": model_name,
            "periods": [1,2,3]
        }
    }
    response = lambda_handler(event, {})
    r = json.loads(response)
    y_pred = pd.read_json(r['predictions'], orient=JSON_ORIENT)
    assert y_pred.shape == (3, 1)
    assert isinstance(y_pred.index, pd.DatetimeIndex)


@pytest.mark.parametrize(
    "model_name", 
    MODEL_LIST
)
def test_handler_predict_by_dates(model_name):
    dates = pd.PeriodIndex(["2017-02", "2017-03", "2017-04"], freq="M")
    dates = dates.astype(str).to_list()
    event = {
        "task": "predict_by_dates",
        "data": {
            "model": model_name,
            "dates": dates,
        }
    }
    response = lambda_handler(event, {})
    r = json.loads(response)
    y_pred = pd.read_json(r['predictions'], orient=JSON_ORIENT)
    assert y_pred.shape == (3, 1)
    assert isinstance(y_pred.index, pd.DatetimeIndex)