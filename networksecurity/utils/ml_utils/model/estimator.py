import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model 
        except Exception as e:
            raise CustomException(e,sys)

    def predict(self,x):
        try:
            X_transform = self.preprocessor.transform(x)
            y_hat = self.preprocessor.predict(X_transform)
            return y_hat 
        except Exception as e:
            raise CustomException(e,sys)