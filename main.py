from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataValidationConfig
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

    except Exception as e:
            raise NetworkSecurityException(e, sys)