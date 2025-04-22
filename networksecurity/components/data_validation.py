import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.exception.customlogging.logger import logging

from scipy.stats import ks_2samp ##Check 2 samples of data to see whether data drift or not.
