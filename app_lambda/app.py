import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Entrypoint for lambda function"""
    logger.debug('## ENVIRONMENT VARIABLES')
    logger.debug(os.environ)
    logger.debug('## EVENT')
    logger.debug(event)
    
    response = {
        "message": 'Hello world, this is a test function!',
        "event": event,
    }
    return json.dumps(response)
