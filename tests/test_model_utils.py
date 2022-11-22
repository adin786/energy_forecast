from pathlib import Path

import pytest
from sktime.base import BaseEstimator
from sktime.forecasting.naive import NaiveForecaster

from energy_forecast.app_lambda.model_utils import get_estimator

TEST_MODEL = Path.cwd() / "models" / "naive.zip"


@pytest.fixture
def loaded_model() -> BaseEstimator:
    return get_estimator(TEST_MODEL)


def test_model_from_path(loaded_model):
    assert isinstance(loaded_model, BaseEstimator)
    assert isinstance(loaded_model, NaiveForecaster)
