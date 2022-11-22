"""Tests whether the locally running lambda image container (prerequisite)
is responding to requests properly

Run the container before testing, with:
docker build -f Dockerfile.lambda -t lambda_test .
docker run -p 9000:8080 lambda_test
"""
import pytest
import requests
from requests.exceptions import ConnectionError

# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'


slow_test = pytest.mark.skipif(
    "not config.getoption('--run-slow')",
    reason="Only run when --run-slow is given",
)


@slow_test
def test_lambda_container():
    try:
        response = requests.post(
            "http://localhost:9000/2015-03-31/functions/function/invocations", json="{}"
        )
    except ConnectionError as exc:
        raise ConnectionError(
            "Connection refused, the docker container is probably not running, "
            "use the following commands to launch it:\n"
            "docker build -f Dockerfile.lambda -t lambda_test .\n"
            "docker run -p 9000:8080 lambda_test"
        ) from exc
    response_json = response.json()
    assert isinstance(response_json, dict)
