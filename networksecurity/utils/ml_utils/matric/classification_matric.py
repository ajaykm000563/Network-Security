from networksecurity.entity.artifact_entity import ClassificationMatricArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import os, sys

def get_classification_score(y_true, y_pred) -> ClassificationMatricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_accuracy_score = accuracy_score(y_true, y_pred)
        classification_matric = ClassificationMatricArtifact(model_accuracy_score, model_precision_score, model_recall_score,model_f1_score)
        logging.info(f"Classification matrics: {classification_matric}")
        return classification_matric
    except Exception as e:
        raise CustomException(e, sys) from e