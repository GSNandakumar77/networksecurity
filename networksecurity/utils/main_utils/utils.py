import os,sys
from networksecurity.exception.exception import  NetworkSecurityException
from networksecurity.logging.logger import logging
import yaml
import numpy as np
#import dill
import pickle
import yaml
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    



def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    



def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numpy array data to file 
    file_path: str location of the file to save 
    array: np.array data to save 
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)

    except Exception as e :
        raise NetworkSecurityException(e,sys)
    

"save the pickle file as object "

def save_object(file_path:str,obj:object):
    try:
        logging.info("entered the save_object method of mainUtilis class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of Mainiutils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file{file_path} is not exist")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_numpy_array_data(file_path:str)->np.array:
    """
    load numpy array from the file 
    file_path : str loaction of file to load 
    retrun np.array data loaded"""
    try:

        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)  from e


def evaluate_models(X_train,Y_train,X_test,Y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]
            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)


            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            ## model.fit(X_train,Y_train)
            Y_train_pred=model.predict(X_train)
            Y_test_pred=model.predict(X_test)
            train_model_score=r2_score(Y_train,Y_train_pred)
            test_model_score=r2_score(Y_test,Y_test_pred)
            report[list(models.keys())[i]]=test_model_score

        return report


    except Exception as e:
        raise NetworkSecurityException(e,sys)

