from networksecurity.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,data_validation_config:DataValidationConfig):

        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config)
            logging.info(f"required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns{len(dataframe.columns)}")

            if number_of_columns==len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05):
        try:
            status=True
            report={}
            """
            📌 What Does the p-value Represent?
                It’s the probability of observing the data assuming the null hypothesis is true (i.e., both samples come from the same distribution).

High p-value → samples are similar → No drift.

Low p-value → samples are statistically different → Drift detected."""

            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found=False

                else:
                    is_found=True
                    status=False
                    report.update({column:{
                        "P_value":float(is_sample_dist.pvalue),
                        "drift_status":is_found

                    }})    


            drift_report_file_path=self.data_validation_config.drift_report_file_path
            #create directory
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys) 




    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numeric_df = dataframe.select_dtypes(include=['number'])
            return numeric_df.shape[1] == dataframe.shape[1]
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        """
        arrow -> Type indicates the expected return type of a function."""
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #read the data froom train and test
            train_data_frame=DataValidation.read_data(train_file_path)
            test_data_frame=DataValidation.read_data(test_file_path)

            # validate number of colums

            status=self.validate_number_of_columns(train_data_frame)
            if not status:
                error_message= f"Train dataframes does not contain  all columns.\n"
            status=self.validate_number_of_columns(test_data_frame)
            if not status:
                error_message= f"Test dataframes does not contain  all columns.\n"    



            train_status =self.is_numerical_column_exist(train_data_frame)
            if not train_status:
                error_message1=f"Numerical columns are missing in the Training dataframe"

            test_status =self.is_numerical_column_exist(test_data_frame)
            if not test_status:
                error_message=f"Numerical columns are missing in the Testing dataframe"


            
            ##lets check datadrift
            status=self.detect_dataset_drift(base_df=train_data_frame,current_df=test_data_frame)    
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)


            train_data_frame.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_data_frame.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            

            data_validation_artifact=DataValidationArtifact(validation_status=status,
                                                           valid_train_file_path=self.data_validation_config.valid_train_file_path,
                                                           valid_test_file_path=self.data_validation_config.valid_test_file_path,
                                                           invalid_train_File_path=None,
                                                            invalid_test_file_path=None,
                                                            drift_report_file_path=self.data_validation_config.drift_report_file_path)
            
            

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)