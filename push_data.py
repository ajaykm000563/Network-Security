import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import numpy as np
import pandas as pd
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException


class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.db = self.client['network_security']
            self.collection = self.db['network_data']
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise CustomException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {e}")
            raise CustomException(e, sys)
        
    def insert_data_to_mongodb(self, records,database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info(f"Data inserted successfully into MongoDB collection: {self.collection}")
            return (len(self.records))
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")
            raise CustomException(e, sys)



if __name__ == "__main__":
   FILE_PATH = "Network_Data\phisingData.csv"
   database = "Network_Security"
   collection = "Network_Data"
   networkobject = NetworkDataExtract()
   records = networkobject.csv_to_json_converter(file_path=FILE_PATH)
   print(records)
   no_of_records = networkobject.insert_data_to_mongodb(records, database, collection)
   logging.info(f"Total number of records inserted: {no_of_records}")
   print(f"Total number of records inserted: {no_of_records}")