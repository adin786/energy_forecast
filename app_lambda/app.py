import json
import os
from loguru import logger
import sys

# logger.remove()
logger.add(sys.stderr, filter=__name__, level="DEBUG")


class LambdaInputError(Exception):
    """Raise if something wrong with the handler event input"""


def lambda_handler(event, context):
    """Entrypoint for lambda function
    Acts a distributor for different tasks depending on the 
    supplied 'task' field"""
    logger.debug("## ENVIRONMENT VARIABLES")
    logger.debug(os.environ)
    logger.debug("## EVENT")
    logger.debug(event)

    if not "task" in event:
        raise LambdaInputError("Missing 'task' field in event")
    else:
        task = event["task"]

    if task == 'hello_world':
        response = {
            "task": task,
            "data": "Hello world, this is a test function!",
            "event": event,
        }
    elif task == 'echo':
        response = {
            "task": task,
            "data": event["data"],
            "event": event,
        }
    else:
        response = {
            "task": task,
            "data": "Unrecognised task",
            "event": event,
        }

    return json.dumps(response)
