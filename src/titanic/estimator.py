from sagemaker.sklearn.estimator import SKLearn
import os

FRAMEWORK_VERSION = "0.23-1"

role = os.environ.get("SAGEMAKER_ROLE")

sklearn_estimator = SKLearn(
    entry_point="src/titanic/script.py",
    role=role,
    instance_count=1,
    instance_type="ml.m4.xlarge",
    framework_version=FRAMEWORK_VERSION,
    base_job_name="rf-scikit",
    hyperparameters={
        "n-estimators": 100,
        "features": "Pclass Sex SibSp Parch",
        "target": "Survived",
    },
)

sklearn_estimator.fit({"train": "s3://ml-deploy-bucket-1001/titanic/train.csv",
                       "test": "s3://ml-deploy-bucket-1001/titanic/test.csv"})