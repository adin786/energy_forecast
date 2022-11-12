"""
It works!
Assumes we have AWS CLI configured with credentials already
"""
from energy_forecast.deploy.aws_lambda import invoke_lambda_function

if __name__ == "__main__":
    payload = {"something": "1111111-222222-333333-bba8-1111111"}
    response = invoke_lambda_function(function_name="energy_forecast", payload=payload)
    print(f"response:{response}")
    print(response)
    print(type(response))
