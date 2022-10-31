from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.base import ForecastingHorizon
import pandas as pd
from typing import Optional
from time import perf_counter
from loguru import logger
import sys
import mlflow
from contextlib import redirect_stdout, redirect_stderr
import pickle
import tempfile
from pathlib import Path
from ..utils import repo_root
import shutil


logger.remove()
logger.add(sys.stderr, filter=__name__, level='DEBUG')
REPO_ROOT = Path(repo_root())


class Model:
    def __init__(self, estimator, *args, **kwargs) -> None:
        self.model = estimator(*args, **kwargs)
        self.params = self.model.get_params(deep=True)
        self.run_name = ''
        logger.debug('INIT: model intialised')
        
    def fit(self, 
            y_train: Optional[pd.DataFrame] = None,
            x_train: Optional[pd.DataFrame] = None,
            y_test: Optional[pd.DataFrame] = None, 
            x_test: Optional[pd.DataFrame] = None, 
            experiment_id: Optional[str] = None,
           ) -> None:
        # May need to handle optional x
        # Some models dont use exogenous variables
        logger.debug('FIT: running .fit() method')
        exogenous = False if (x_train is None) else True
        if exogenous:
            logger.debug(f'FIT: {y_train.shape=}, {x_train.shape}')
        else:
            logger.debug(f'FIT: {y_train.shape=}')

        log_dir = (REPO_ROOT / 'logs')
        if log_dir.exists():
            shutil.rmtree(log_dir)
            logger.debug(f'FIT: existing log_dir deleted: {log_dir}')
        log_dir.mkdir()
        logger.debug(f'FIT: new log_dir created: {log_dir}')
        logger.debug('FIT: creating stdout.log and stderr.log in log_dir')
        
        # May need to handle setting experiment etc
        with (
            mlflow.start_run(experiment_id=experiment_id) as run,
            open(log_dir / 'stdout.log', 'w') as f1, 
            open(log_dir / 'stderr.log', 'w') as f2,
            ):
            self.run_name = run

            with redirect_stdout(f1), redirect_stderr(f2):
                logger.add(sys.stderr, filter=__name__, level='DEBUG')

                logger.debug('FIT: starting mlflow tracking')
                mlflow.log_params(self.params)
                logger.debug(f'FIT: model params tracked ({len(self.params)} values)')
                
                logger.debug('FIT: training model')
                t0 = perf_counter()
                if exogenous:
                    self.model.fit(y_train)
                else:
                    self.model.fit(y_train, x_train)
                t1 = perf_counter()
                mlflow.log_metric('train_time', t1 - t0)
                logger.debug(f'FIT: finished training model, took {t1-t0:.2f} seconds')
                # mlflow.sklearn.log_model(self.model, 'model')
                logger.debug('FIT: tracked model artefact')
                
                # Evaluate
                fh = ForecastingHorizon(y_test.index, is_relative=False)
                if exogenous:
                    y_pred = self.model.predict(fh, x_test)
                else:
                    y_pred = self.model.predict(fh)

                if exogenous:
                    score = self.model.score(y_test, x_test)
                else:
                    score = self.model.score(y_test)
                logger.debug(f'EVAL: {score=:.3f}')
                mlflow.log_metric('score_mape', score)

                # Upload logs
                mlflow.log_artifact(log_dir / 'stdout.log')
                mlflow.log_artifact(log_dir / 'stderr.log')


                
                
                
            
            
        
    