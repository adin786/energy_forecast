"""
Quick test to check that the lambda function works
Uses boto3 behind the scenes.
"""
from energy_forecast.deploy.aws_lambda import invoke_lambda_function

if __name__ == "__main__":
    payload = {"something": "1111111-222222-333333-bba8-1111111"}
    response = invoke_lambda_function(function_name="energy_forecast", payload=payload)
    print(f"response:{str(response)}")
    print(response)
    print(type(response))
