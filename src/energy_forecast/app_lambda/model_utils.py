from typing import Iterable
from sktime.base import load, BaseEstimator
from sktime.forecasting.base import ForecastingHorizon
import pandas as pd
from pathlib import Path
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, filter=__name__, level="INFO")


class ModelDataNotFound(Exception):
    """Raise if serialised model file does not exist"""


def get_estimator(path: str):
    path = Path(path)
    if path.is_file():
        estimator = load(path)
    else:
        raise ModelDataNotFound(f"Sktime model data (.zip) was not found: {path}")
    return estimator


# def get_prediction(model)


class DeployedSktimeModel:
    def __init__(self, estimator: BaseEstimator) -> None:
        self.estimator = estimator

    @classmethod
    def load(cls, path: str) -> "DeployedSktimeModel":
        """Construct class from file path using sktime.base.load.
        I did it this way to allow alternative serialisation"""
        estimator = get_estimator(path)
        return cls(estimator)

    def predict_by_periods(self, periods: Iterable) -> float:
        """Gives prediction for an list or array of ints, each representing
        the number of forward steps to predict at.
        Try `np.arange(x)+1` for a range.  Or [1] for 1 step forward"""
        if not isinstance(periods, Iterable):
            raise ValueError("Must be an iterable")
        if any([x < 1 for x in periods]):
            raise ValueError("periods must be >= 1")
        fh = ForecastingHorizon(periods, is_relative=True)
        return self.estimator.predict(fh)

    def predict_by_dates(self, date: Iterable) -> float:
        """Gives prediction at a provided input index.  Must be PeriodIndex etc.
        Use `pd.PeriodIndex(["YYYY-MM"], freq="M")` for example"""
        fh = ForecastingHorizon(date, is_relative=False)
        return self.estimator.predict(fh)
