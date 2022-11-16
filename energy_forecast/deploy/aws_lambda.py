import boto3
from botocore.errorfactory import ResourceNotFoundException
import json
import typing


class LambdaOfflineError(Exception):
    """Raise if lambda function did not exist"""


def invoke_lambda_function(
    function_name: str, payload: typing.Mapping[str, str] = None
) -> bytes:
    """Helper function to allow easy invokations of a deployed lambda function
    https://stackoverflow.com/a/59626441/19357935"""
    if function_name is None:
        raise Exception("ERROR: function_name parameter cannot be NULL")

    payload_str = json.dumps(payload)
    payload_bytes = bytes(payload_str, encoding="utf8")
    client = boto3.client("lambda")
    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=payload_bytes,
        )
    except ResourceNotFoundException:
        raise LambdaOfflineError("Looks like the lambda function is not deployed yet")

    response = json.loads(response["Payload"].read())
    return json.loads(response)
