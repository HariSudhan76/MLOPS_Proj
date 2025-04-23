import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging 
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)        
        with open(file_path,"w") as file:
            yaml.safe_dump(content, file,default_flow_style=False, 
            allow_unicode=True, 
            sort_keys=False)
    except Exception as e:
        raise CustomException(e,sys)