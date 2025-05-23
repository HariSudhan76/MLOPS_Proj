import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.constant import training_pipeline

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config) 
            logging.info("start data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            
            logging.info("Initiate the data validation")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Initiate the data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config = data_transformation_config)

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_training_config = ModelTrainerConfig(self.training_pipeline_config)
            model_training = ModelTrainer(data_transformation_artifact,model_training_config)
            model_training_artifact = model_training.initiate_model_trainer()
            return model_training_artifact
        except Exception as e:
            raise CustomException(e,sys)
    ##local artifact is going to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{training_pipeline.TRAINING_BUCKET_NAME}/artifact{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
    ##local final model is pushed to s3 buckt
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{training_pipeline.TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)
    