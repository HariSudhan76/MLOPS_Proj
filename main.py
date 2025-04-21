import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig

if __name__=='__main__':
    try:
        tpc = TrainingPipelineConfig()
        dic = DataIngestionConfig(tpc)
        di = DataIngestion(dic)
        logging.info("Enter the try block")
        dia = di.initiate_data_ingestion()
        print(dia)    
    except Exception as e:
        raise CustomException(e,sys)

