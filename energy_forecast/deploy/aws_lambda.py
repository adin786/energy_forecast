import boto3
import json
import typing


def invoke_lambda_function(
    function_name: str, 
    payload: typing.Mapping[str, str] = None
) -> bytes:
    """Helper function to allow easy invokations of a deployed lambda function
    https://stackoverflow.com/a/59626441/19357935"""
    if function_name is None:
        raise Exception("ERROR: function_name parameter cannot be NULL")

    payload_str = json.dumps(payload)
    payload_bytes = bytes(payload_str, encoding="utf8")
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=payload_bytes,
    )
    response = json.loads(response['Payload'].read())
    return json.loads(response)
