"""
It works!
Assumes we have AWS CLI configured with credentials already
"""
import boto3, json, typing

def invokeLambdaFunction(*, functionName:str=None, payload:typing.Mapping[str, str]=None):
    """https://stackoverflow.com/a/59626441/19357935"""
    if functionName == None:
        raise Exception('ERROR: functionName parameter cannot be NULL')
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    client = boto3.client('lambda')
    return client.invoke(
        FunctionName=functionName,
        InvocationType="RequestResponse",
        Payload=payloadBytesArr
    )

if __name__ == '__main__':
    payloadObj = {"something" : "1111111-222222-333333-bba8-1111111"}
    response = invokeLambdaFunction(functionName='hello-world',  payload=payloadObj)
    print(f'response:{response}')
    print(response["Payload"].read())