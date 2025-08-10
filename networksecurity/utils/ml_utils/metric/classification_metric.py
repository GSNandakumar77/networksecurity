from sklearn.metrics import f1_score,precision_score,recall_score
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
import sys

def get_classification_score(Y_true,Y_pred)->ClassificationMetricArtifact:
    try:

        model_f1_score=f1_score(Y_true,Y_pred)
        model_recall_Score=recall_score(Y_true,Y_pred)
        model_precision_score=precision_score(Y_true,Y_pred)

        classification_metric=ClassificationMetricArtifact(
            precision_score=model_precision_score,
            recall_score=model_recall_Score,
            f1_score=model_f1_score
        )
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)