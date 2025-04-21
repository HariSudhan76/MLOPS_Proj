import os
import sys 
import json 
from dotenv import load_dotenv
import pymongo.mongo_client
load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")
import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def cv_to_json_convertor(self,filepath):
        try:
        
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise CustomException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise CustomException(e,sys)
    
    
if __name__=='__main__':
    filepath = 'Network_Data\\phisingData.csv'
    database = "gharisudhan76"
    collection = "NetworkData"
    extractor = NetworkDataExtract()
    records = extractor.cv_to_json_convertor(filepath)
    no_of_records = extractor.insert_data_mongodb(records, database,collection)
    print(no_of_records)
  
        