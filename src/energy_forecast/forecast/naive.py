from sktime.forecasting.naive import NaiveForecaster
import pandas as pd
from typing import Optional
from time import perf_counter
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, filter=__name__, level='DEBUG')


class Model:
    def __init__(self, estimator, *args, **kwargs) -> None:
        self.model = estimator(*args, **kwargs)
        self.params = self.model.get_params(deep=True)
        self.run_name = ''
        logger.debug('INIT: model intialised')
        
    def fit(self, 
            y_train: Optional[pd.DataFrame],
            x_train: Optional[pd.DataFrame],
            y_test: Optional[pd.DataFrame], 
            x_test: Optional[pd.DataFrame], 
           ) -> None:
        # May need to handle optional x
        # Some models dont use exogenous variables
        logger.debug('FIT: running .fit() method')
        exogenous = False if (x_train is None) else True
        if exogenous:
            logger.debug(f'FIT: {y_train.shape=}, {x_train.shape}')
        else:
            logger.debug(f'FIT: {y_train.shape=}')
        
        # May need to handle setting experiment etc
        with mlflow.start_run(), open('stdout.log', 'w') as f1, open('stderr.log', 'w') as f2:
            self.run_name = mlflow.get_run_name()
            with redirect_stdout(f1), redirect_stderr(f2):
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
                
                # Evaluate
                fh = ForecastHorizon(y_test.index)
                if exogenous:
                    y_pred = self.model.predict(fh, x_test)
                else:
                    y_pred = self.model.predict(fh)
                
                
            
            
        
    