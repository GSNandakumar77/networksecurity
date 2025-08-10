from networksecurity.components.data_ingestion import DataIngestion
import sys,os
import numpy as np 
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object 


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            if 'Unnamed: 0' in df.columns:
                df.drop('Unnamed: 0', axis=1, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
  



    def get_data_transformer_object(self)->Pipeline:
        """
         It initialises a knn imputer object with the parameter we specified in the training_pipeline.py file 
         and returns a Pipeline object with the knn imputer object as the first step 
         ARGS:
         cls : Datatransformation

         Returns :
         A pipeline object 
        
        """
        logging.info("Enter the get_datatransformer method of the cls DataTransformation ")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)## ** consider as key value pair paramter from training.py file 
            logging.info(f"Initialised Knn imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS} ")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        




    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered inititate_data_transfromation method of datatransformation class")
        try:
            logging.info("Data trnsformation started")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #training_dataframe like X_train,Y_train
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            #testing dataframe like X_test,Y_test
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer_object() 
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)

            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            ##saving the preprocessor object in the seperate folder
            save_object("final_models/preprocessor.pkl",preprocessor_object)
            ##prepaaring artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)