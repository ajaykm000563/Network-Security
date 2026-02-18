from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataValidationConfig,DataTransformationConfig,DataIngestionConfig,TrainingPipelineConfig,ModelTrainerConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,DataIngestionArtifact,ModelTrainerArtifact
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
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
        
        logging.info("Starting data transformation")
        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        datatransformation = DataTransformation(datavalidationartifact, datatransformationconfig)
        datatransformationartifact = datatransformation.initiate_data_transformation()
        logging.info("Data transformation completed successfully")
        
        logging.info("Model training started")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config, datatransformationartifact)
        modeltrainerartifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed successfully")
        print(modeltrainerartifact)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise CustomException(e, sys)