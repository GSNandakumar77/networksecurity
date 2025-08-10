from networksecurity.constants.training_pipeline import MODEL_FILE_NAME,SAVED_MODEL_DIR

import os
import sys 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def predict(self,x):
        try:
            x_transformed=self.preprocessor(x)
            Y_hat=self.model.predict(x_transformed)
            return Y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)