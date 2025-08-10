import os 
import sys


from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,RandomForestClassifier,GradientBoostingClassifier
)

import dagshub
dagshub.init(repo_owner='GSNandakumar77', repo_name='networksecurity', mlflow=True)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self, best_model, classification_metric, log_model_flag=False):
        with mlflow.start_run(nested=True):
            mlflow.log_metric("f1_Score", classification_metric.f1_score)
            mlflow.log_metric("precision_score", classification_metric.precision_score)
            mlflow.log_metric("recall_score", classification_metric.recall_score)

            if log_model_flag:  # save only if True
                model_path = "best_model"
                if os.path.exists(model_path):
                    import shutil
                    shutil.rmtree(model_path)
                mlflow.sklearn.save_model(best_model, model_path)
                mlflow.log_artifacts(model_path, artifact_path="model")




    def train_model(self,X_train,Y_train,X_test,Y_test):
        models={
            "Random Forest":RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Logistic Regression":LogisticRegression(),
            "AdaBoost": AdaBoostClassifier()
        }
        
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        model_report:dict=evaluate_models(X_train,Y_train,X_test,Y_test,
                                          models=models,params=params)
        ## to get best model score from dict 
        best_model_score=max(sorted(model_report.values()))



        ## to get the best model name 
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)]
        

        best_model=models[best_model_name]
        Y_train_pred=best_model.predict(X_train)
        Y_test_pred=best_model.predict(X_test)

        classification_train_metric=get_classification_score(Y_true=Y_train,Y_pred=Y_train_pred)
        

        ##track the experiment end to end level with  mlflow -->
        self.track_mlflow(best_model,classification_train_metric)




        Y_test_pred=best_model.predict(X_test)
        classification_test_metric=get_classification_score(Y_true=Y_test,Y_pred=Y_test_pred)



        self.track_mlflow(best_model,classification_test_metric)


        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)



        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        ## save the model_object in seperate folder 
        save_object("final_models/model.pkl",best_model)
        ##model trainer artifacts 

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                            train_metric_artifact= classification_train_metric,
                            test_metric_artifact=classification_test_metric)
        
        logging.info(f"Model trainer artifacts:{model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self):
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path


            #loading training array and testing array 
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            
            X_train,Y_train,X_test,Y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )


            model=self.train_model(X_train,Y_train,X_test,Y_test)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
