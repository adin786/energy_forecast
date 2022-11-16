from sktime.forecasting.base import ForecastingHorizon
from sktime import base
from sktime.utils.plotting import plot_series
import pandas as pd
import numpy as np
from typing import Iterable, Optional
from time import perf_counter
from loguru import logger
import sys
import mlflow
import matplotlib.pyplot as plt
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from .utils import repo_root
import shutil


LEVEL = "WARNING"
logger.remove()
logger.add(sys.stderr, filter=__name__, level=LEVEL)
REPO_ROOT = Path(repo_root())


def check_experiment_exists(exp_name: str) -> bool:
    """Returns true if experiment name exists in mlflow.search_experiments"""
    exp_exists = False
    list_exp = [e.name for e in mlflow.search_experiments()]
    if exp_name not in list_exp:
        exp_exists = True
    return exp_exists


def dedup_dict(params: dict) -> dict:
    """Small hack to get around an issue with mlflow.log_param
    when duplicate param names exist (case insensitive duplicates)"""
    seen_keys = []
    new_dict = {}
    for k, v in params.items():
        if k.lower() in seen_keys:
            new_dict[k+"_"] = v
        else:
            new_dict[k] = v
        seen_keys.append(k.lower())
    return new_dict


class Model:
    """Sktime model wrapper to enable mlflow tracked runs"""

    def __init__(
        self,
        estimator: base.BaseEstimator,
        name: Optional[str] = None,
    ) -> None:
        self.model = estimator
        self.params = dedup_dict(self.model.get_params(deep=True))
        self.name = name
        self.tmp_logger = None
        self.score = None
        logger.remove()
        logger.remove(self.tmp_logger)
        logger.add(sys.stderr, filter=__name__, level=LEVEL)
        logger.debug("INIT: model intialised")
        logger.info(f"INIT: params {self.params}")

    def save(self, path: str) -> None:
        """Serialise to .zip file using sktime method"""
        self.model.save(path)

    @classmethod
    def load(cls, path: str, name: str) -> "Model":
        """Load from .zip file using sktime method"""
        estimator = base.load(path)
        return cls(estimator, name)

    def fit_and_evaluate(
        self,
        y_train: Optional[pd.DataFrame] = None,
        x_train: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.DataFrame] = None,
        x_test: Optional[pd.DataFrame] = None,
        exp_name: Optional[str] = None,
        ) -> None:
        # May need to handle optional x
        # Some models dont use exogenous variables
        logger.remove()
        logger.remove(self.tmp_logger)
        logger.add(sys.stderr, filter=__name__, level=LEVEL)
        logger.debug("FIT: running .fit() method")
        exogenous = False if (x_train is None) else True
        if exogenous:
            logger.debug(f"FIT: {y_train.shape=}, {x_train.shape}")
        else:
            logger.debug(f"FIT: {y_train.shape=}")

        log_dir = REPO_ROOT / "logs"
        if log_dir.exists():
            shutil.rmtree(log_dir)
            logger.debug(f"FIT: existing log_dir deleted: {log_dir}")
        log_dir.mkdir()
        logger.debug(f"FIT: new log_dir created: {log_dir}")
        logger.debug("FIT: creating stdout.log and stderr.log in log_dir")

        if check_experiment_exists(exp_name):
            exp_id = mlflow.create_experiment(exp_name)
        else:
            exp = mlflow.get_experiment_by_name(exp_name)
            exp_name = exp.name
            exp_id = exp.experiment_id

        # Fix dtype for Prophet models
        if self.model.__class__.__name__ == 'Prophet':
            y_train = y_train.to_timestamp()
            y_test = y_test.to_timestamp()

        # May need to handle setting experiment etc
        with (
            mlflow.start_run(experiment_id=exp_id, run_name=self.name) as run,
            open(log_dir / "stdout.log", "w") as f1,
            open(log_dir / "stderr.log", "w") as f2,
            ):
            self.run_name = run

            with redirect_stdout(f1), redirect_stderr(f2):
                # self.tmp_logger = logger.add(sys.stderr, filter=__name__, level=LEVEL)

                logger.debug("FIT: starting mlflow tracking")
                mlflow.log_params(self.params)
                logger.debug(f"FIT: model params tracked ({len(self.params)} values)")

                logger.debug("FIT: training model")
                t0 = perf_counter()
                if exogenous:
                    self.model.fit(y_train)
                else:
                    self.model.fit(y_train, x_train)
                t1 = perf_counter()
                mlflow.log_metric("train_time", t1 - t0)
                logger.info(f"FIT: finished training model, took {t1-t0:.2f} seconds")
                # mlflow.sklearn.log_model(self.model, 'model')
                logger.debug("FIT: tracked model artefact")

                # Evaluate

                # if exogenous:
                #     score = self.get_score(y_test, x_test)
                # else:
                score = self.get_score(y_test)
                logger.info(f"EVAL: {score=:.3f}")
                mlflow.log_metric("score_mape", score)

                fig = self.plot_evaluation(y_train, y_test)
                mlflow.log_figure(fig, 'plot.png')

                # Upload logs
                mlflow.log_artifact(log_dir / "stdout.log")
                mlflow.log_artifact(log_dir / "stderr.log")

    def get_score(
        self,
        y_eval: Optional[pd.DataFrame] = None,
        x_eval: Optional[pd.DataFrame] = None,
        ) -> float:
        # exogenous = False if (x_eval is None) else True
        # if exogenous:
        #     score = self.model.score(y_eval, X=x_eval, fh=y_eval.index)
        # else:
        score = self.model.score(y_eval, X=x_eval, fh=y_eval.index)
        self.score = score
        logger.info(f"EVAL: {score=:.3f}")
        return score


    def predict_by_periods(self, periods: Iterable) -> float:
        """Gives prediction for an list or array of ints, each representing 
        the number of forward steps to predict at.
        Use `np.arange(x)+1` for a range.  Or [1] for 1 step forward"""
        if not isinstance(periods, Iterable):
            raise ValueError('Must be an iterable')
        if any([x < 1 for x in periods]):
            raise ValueError('periods must be >= 1')
        fh = ForecastingHorizon(periods, is_relative=True)
        return self.model.predict(fh)


    def predict_by_dates(self, date: Iterable) -> float:
        """Gives prediction at a provided input index.  Must be PeriodIndex etc.
        Use `pd.PeriodIndex(["YYYY-MM"], freq="M")` for example"""
        fh = ForecastingHorizon(date, is_relative=False)
        return self.model.predict(fh)

    
    def plot_evaluation(self, y_train: pd.DataFrame, y_test: pd.DataFrame) -> None:
        y_pred = self.predict_by_dates(y_test.index)
        fig, ax = plot_series(
            y_train, 
            y_test, 
            y_pred, 
            labels=["train", "test", "predictions"]
        )
        return fig

