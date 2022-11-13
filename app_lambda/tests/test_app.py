import pytest
import json
from ..app import lambda_handler
from loguru import logger
import sys

# logger.remove()
logger.add(sys.stderr, filter=__name__, level="DEBUG")


def test_handler_hello():
    event = {
        "task": "hello_world",
        "data": "Some data",
        }
    context = None
    response = lambda_handler(event, context)
    logger.debug(f'{response=}')
    response_dict = json.loads(response)
    logger.debug(f'{response_dict=}')
    assert isinstance(response, str)
    assert isinstance(response_dict, dict)


def test_handler_echo():
    some_data = "Some data"
    event = {
        "task": "echo",
        "data": some_data,
        }
    context = None
    response = lambda_handler(event, context)
    logger.debug(f'{response=}')
    response_dict = json.loads(response)
    logger.debug(f'{response_dict=}')
    assert isinstance(response, str)
    assert isinstance(response_dict, dict)
    assert "data" in response_dict
    assert response_dict["data"] == some_data