from pathlib import Path
import pytest
from sktime.base import load, BaseEstimator
from sktime.forecasting.naive import NaiveForecaster

# from ..model_utils import

TEST_MODEL = Path(__file__).parent / "test_model.zip"


@pytest.fixture
def loaded_model() -> BaseEstimator:
    path = Path(TEST_MODEL)
    if not path.is_file() or path.suffix != ".zip":
        raise FileNotFoundError("Sktime model data (.zip) was not found")
    return load(path)


def test_model_from_path(loaded_model):
    assert isinstance(loaded_model, BaseEstimator)
    assert isinstance(loaded_model, NaiveForecaster)
