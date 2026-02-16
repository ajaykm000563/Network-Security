from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import os, sys
import pandas as pd
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys) from e
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys) from e
    
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            # Extract column names from schema (list of dicts → list of keys)
            schema_columns = [list(col.keys())[0] for col in self._schema_config["columns"]]

            missing_cols = [col for col in schema_columns if col not in dataframe.columns]
            extra_cols = [col for col in dataframe.columns if col not in schema_columns]

            logging.info(f"Schema columns count: {len(schema_columns)}")
            logging.info(f"Dataframe columns count: {len(dataframe.columns)}")
            logging.info(f"Missing columns: {missing_cols}")
            logging.info(f"Extra columns: {extra_cols}")

            if missing_cols:
                return False

            return True

        except Exception as e:
            raise CustomException(e, sys) from e



    
    
    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if is_same_dist.pvalue >= threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,replace=True)
            return status
        except Exception as e:
            raise CustomException(e,sys) from e
         
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path
            
            # Reading the train and test dataframes
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # Validating the the number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                raise CustomException(f"Train dataframe does not have all columns",sys)
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                raise CustomException(f"Test dataframe does not have all columns",sys)
            
            #Checking the data drift 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            #Saving the report and the valid train and test files
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifact = DataValidationArtifact(
            validation_status=status,
            valid_train_file_path=self.data_ingestion_artifact.training_file_path,
            valid_test_file_path=self.data_ingestion_artifact.testing_file_path,
            invalid_train_file_path=None,
            invalid_test_file_path=None,
            drift_report_file_path=self.data_validation_config.drift_report_file_path)
            return data_validation_artifact
           
        except Exception as e:
            raise CustomException(e,sys) from e    