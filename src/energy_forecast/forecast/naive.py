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
        
    def fit(self, y: Optional[pd.DataFrame], x: Optional[pd.DataFrame]) -> None:
        # May need to handle optional x
        # Some models dont use exogenous variables
        
        # May need to handle setting experiment etc
        with mlflow.start_run(), open('stdout.log', 'w') as f1, open('stderr.log', 'w') as f2:
            with redirect_stdout(f1), redirect_stderr(f2):
                logger.debug('FIT: starting mlflow tracking')
                mlflow.log_params(self.params)
                logger.debug(f'FIT: model params tracked ({len(self.params)})')
                
                t0 = perf_counter()
                self.model.fit(y, x)
                t1 = perf_counter()
                mlflow.log_metric('train_time', t1 - t0)
                
            
            
        
    