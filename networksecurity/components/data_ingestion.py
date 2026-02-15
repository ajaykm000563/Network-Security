from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

# Configuration for data ingestion 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from typing import List

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(f"Error initializing DataIngestion: {e}")
            raise CustomException(e, sys)
        
        
        
    def export_collection_as_dataframe(self):
        """
           Reading data from MongoDB collection and converting it to DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df.drop("_id", axis=1, inplace=True)
            df.replace({"nan": np.nan}, inplace=True)    
            logging.info(f"Data exported successfully from MongoDB collection: {collection_name}")
            return df
        except Exception as e:
            logging.error(f"Error exporting collection as DataFrame: {e}")
            raise CustomException(e, sys)
        
        
    
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data exported successfully into feature store file: {feature_store_file_path}")
            return dataframe
        except Exception as e:
            logging.error(f"Error exporting data into feature store: {e}")
            raise CustomException(e, sys)   
        
        
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            
            logging.info(f"Data split into train and test sets successfully with test size: {self.data_ingestion_config.train_test_split_ratio}")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test sets to file paths: {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            
            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f"Train and test sets exported successfully to file paths: {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")
        except Exception as e:
            logging.error(f"Error splitting data into train and test sets: {e}")
            raise CustomException(e, sys)    
        
        
        
    def initiate_data_ingestion(self):
        try:
           dataframe = self.export_collection_as_dataframe()
           dataframe = self.export_data_into_feature_store(dataframe=dataframe)
           self.split_data_as_train_test(dataframe=dataframe)
           dataingetionartifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path, testing_file_path=self.data_ingestion_config.testing_file_path)
           logging.info(f"Data ingestion completed successfully with artifact: {dataingetionartifact}")
           return dataingetionartifact
        except Exception as e:
            logging.error(f"Error in initiate_data_ingestion: {e}")
            raise CustomException(e, sys)    