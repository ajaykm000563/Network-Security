from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import TrainingPipelineConfig
import os
import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Exporting collection as DataFrame")
        dataingetionartifact = data_ingestion.initiate_data_ingestion()
        
        logging.info("Starting data validation")
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(datavalidationconfig, dataingetionartifact)
        datavalidationartifact = datavalidation.initiate_data_validation()
        logging.info("Data validation completed successfully")
        print(datavalidationartifact)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise CustomException(e, sys)