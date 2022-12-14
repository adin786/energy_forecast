import json
import os
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from .model_utils import DeployedSktimeModel

logger.remove()
logger.add(sys.stderr, filter=__name__, level="DEBUG")

HELLO_WORLD = "hello_world"
ECHO = "echo"
PREDICT_BY_PERIODS = "predict_by_periods"
PREDICT_BY_DATES = "predict_by_dates"
JSON_ORIENT = "index"


class LambdaInputError(Exception):
    """Raise if something wrong with the handler event input"""


def lambda_handler(event: dict, context=None) -> dict:
    """Entrypoint for lambda function
    Acts a distributor for different tasks depending on the
    supplied 'task' field"""
    logger.debug(f"ENV: {os.environ}")
    logger.debug(f"EVENT: {event}")
    logger.debug(f"CONTEXT: {type(context)=}")
    if context is not None:
        logger.debug(f"CONTEXT: {context.function_name}, {context.function_version}")

    if not "task" in event:
        logger.debug("Missing 'task' field in event, running dummy task")
        response = dummy(event)
    else:
        task = event["task"]
        if task == HELLO_WORLD:
            response = hello_world(event)
        elif task == ECHO:
            response = echo(event)
        elif task == PREDICT_BY_PERIODS:
            response = predict_by_periods(event)
        elif task == PREDICT_BY_DATES:
            response = predict_by_dates(event)
        else:
            response = dummy(event)

    if not is_jsonable(response):
        raise TypeError(f"response object was not JSON serialisable: {response}")
    return response


def is_jsonable(x):
    """https://stackoverflow.com/a/53112659/19357935"""
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def dummy(event: dict) -> dict:
    response = {"message": "Invalid task"}
    return response


def hello_world(event: dict) -> dict:
    response = {"message": "Hello world, this is a test function!"}
    return response


def echo(event: dict) -> dict:
    data = event.get("data", "No data supplied")
    response = {"message": data}
    return response


def predict_by_periods(event: dict) -> dict:
    """Expects event["data"] = {
        "model": "naive_seasonal.zip",
        "periods": [1, 2, 3...]
    }

    Use `np.arange(x) + 1` for a continuous range"""
    data = event["data"]
    model_name = data["model"]
    periods = data["periods"]

    model = DeployedSktimeModel.load(Path.cwd() / "models" / model_name)
    y_pred = model.predict_by_periods(periods)
    response = {
        "predictions": y_pred.to_json(orient=JSON_ORIENT),
        "orient": JSON_ORIENT,
    }
    return response


def predict_by_dates(event: dict) -> dict:
    """Expects event["data"] = ["2017-02", "2017-03"...]
    Use `pd.PeriodIndex(["2017-02", "2017-03"...], freq="M")` for a continuous range
    Or `.to_period(freq="M")` method on a pd.DatetimeIndex array"""
    data = event["data"]
    model_name = data["model"]
    dates = data["dates"]
    dates = pd.PeriodIndex(dates, freq="M")

    model = DeployedSktimeModel.load(Path.cwd() / "models" / model_name)

    y_pred = model.predict_by_dates(dates)
    response = {
        "predictions": y_pred.to_json(orient=JSON_ORIENT),
        "orient": JSON_ORIENT,
    }
    return response
