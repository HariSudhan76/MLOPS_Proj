import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation, DataValidationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataTransformationConfig

if __name__=='__main__':
    try:
        tpc = TrainingPipelineConfig()
        dic = DataIngestionConfig(tpc)
        di = DataIngestion(dic)
        logging.info("Initiate the data ingestion")
        dia = di.initiate_data_ingestion()
        # print(dia)    
        logging.info("Data initiation Completed")

        dvc = DataValidationConfig(tpc)
        dv = DataValidation(dia,dvc)
        logging.info("Initiate the data validation")
        dva = dv.initiate_data_validation()
        # print(dva)
        logging.info("data validation completed")


        dtc = DataTransformationConfig(tpc)
        dt = DataTransformation(dva,dtc)
        logging.info("Initiate the data transformation")
        dta = dt.initiate_data_transformation()
        print(dta)
        logging.info("data transformation completed")
    except Exception as e:
        raise CustomException(e,sys)

