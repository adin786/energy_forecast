import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Entrypoint for lambda function"""
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(event)
    
    response = {
        "message": 'Hello world, this is a test function!',
        "event": event,
    }
    return json.dumps(response)