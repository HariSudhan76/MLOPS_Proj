import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation, DataValidationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataTransformationConfig,ModelTrainerConfig


if __name__=='__main__':
    try:
        logging.info("Initiate the data ingestion")
        tpc = TrainingPipelineConfig()
        dic = DataIngestionConfig(tpc)
        di = DataIngestion(dic)
        dia = di.initiate_data_ingestion()
        print(dia)   
        logging.info("Data initiation Completed")
        print("*"*100)

        logging.info("Initiate the data validation")
        dvc = DataValidationConfig(tpc)
        dv = DataValidation(dia,dvc)
        dva = dv.initiate_data_validation()
        print(dva)
        logging.info("data validation completed")
        print("*"*100)

        logging.info("Initiate the data transformation")
        dtc = DataTransformationConfig(tpc)
        dt = DataTransformation(dva,dtc)
        dta = dt.initiate_data_transformation()
        print(dta)
        logging.info("data transformation completed")
        print("*"*100)

        logging.info("Initiate the model training")
        mtc = ModelTrainerConfig(tpc)
        mt = ModelTrainer(model_trainer_config=mtc,data_transformation_artifact=dta)
        mta = mt.initiate_model_trainer()
        print(mta)
        logging.info("Model training completed")
        print("*"*100)


    except Exception as e:
        raise CustomException(e,sys)

