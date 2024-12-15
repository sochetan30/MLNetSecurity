from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig =DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)

        logging.info("Intiate the data ignestion")
        dataingestionartifacts= data_ingestion.initiate_data_ingestion()
        logging.info("Data Intiatio Completed")
        print(dataingestionartifacts)
        datavalidation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifacts, datavalidation_config)
        logging.info("Intiate the data validation")
        data_validation_artifact =data_validation.initiate_data_validation()
        logging.info("Validation Completed")

        print(data_validation_artifact)
        logging.info("Data Transformation Started")
        
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifacts = data_transformation.intiate_data_transformation()

        print(data_transformation_artifacts)
        logging.info("Data Transformation Completed")

    except Exception as e:
            raise NetworkSecurityException(e, sys)