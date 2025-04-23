import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import numpy 
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.customlogging.logger import logging 
from networksecurity.exception.exception import CustomException
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig
                 ):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    def get_data_transformer_object(cls)->Pipeline:
        """
        It intilialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and return a Pipeline object with KNNImputer object as first step.
        Args:
        cls: DataTransformation

        Returns:
        A Pipeline object
        """
        logging.info(
            "Entered get_data_stransformer_object method of transformation class"
        )
        try:
            imputer:KNNImputer= KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) ## ** Means key value pair
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise CustomException(e,sys)    


    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.infor("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            ##training Dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            ##target feature is -1 and 1 so will convert -1 to 0
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ##test Dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,)

        except Exception as e:
            raise CustomException(e,sys)
        
