import json
import os
from typing import Optional
from loguru import logger
import sys
from .model_utils import DeployedSktimeModel
from pathlib import Path
import pandas as pd

logger.remove()
logger.add(sys.stderr, filter=__name__, level="DEBUG")

HELLO_WORLD = "hello_world"
ECHO = "echo"
PREDICT_BY_PERIODS = "predict_by_periods"
PREDICT_BY_DATES = "predict_by_dates"
JSON_ORIENT = "index"


class LambdaInputError(Exception):
    """Raise if something wrong with the handler event input"""


def lambda_handler(event: dict, context: Optional[dict] = None) -> str:
    """Entrypoint for lambda function
    Acts a distributor for different tasks depending on the
    supplied 'task' field"""
    context = context if context is not None else {}
    logger.debug(f"ENV: {os.environ}")
    logger.debug(f"EVENT: {event}")
    logger.debug(f"CONTEXT: {type(context)=}")
    logger.debug(
        f"CONTEXT: {context.get('function_name')}, {context.get('function_version')}"
    )

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

    return json.dumps(response)


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
