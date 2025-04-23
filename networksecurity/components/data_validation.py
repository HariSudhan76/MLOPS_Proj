import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

from scipy.stats import ks_2samp ##Check 2 samples of data to see whether data drift or not.
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifcat = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
    
    @staticmethod ##This decorator make the direct use of below funtion.
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data Frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True 
            return False
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                is_found = threshold>is_same_dist.pvalue
                if is_found:
                    status = False
                report.update({col:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status":bool(is_found)
                    }})
                logging.info(f"{col}-> p-value: {is_same_dist.pvalue}, Drift: {is_found}")
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            #create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifcat.trained_file_path
            test_file_path = self.data_ingestion_artifcat.test_file_path

            ##read the train and test files
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            #Validate number of columns
            status = self.validate_number_of_columns(train_df)
            if not status:
                error_message = "Train dataframe does not contain all columns. \n"
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_message =  "Test dataframe does not contain all columns. \n"
            
            ## lets check datadrift
            status = self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path = self.data_ingestion_artifcat.trained_file_path,
                valid_test_file_path = self.data_ingestion_artifcat.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)