import pandas as pd
import boto3
import sagemaker
import json
import joblib
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# Set SageMaker and S3 client variables
sess = sagemaker.Session()

region = sess.boto_region_name
print("Region:", region)
s3_client = boto3.client("s3", region_name=region)

# sagemaker_role = sagemaker.get_execution_role()
# print("SageMaker Execution Role:", sagemaker_role)

# Set read and write S3 buckets and locations
write_bucket = sess.default_bucket()
write_prefix = "titanic"
print("Write Bucket:", write_bucket)

read_bucket = "ml-deploy-bucket-1001"
read_prefix = "titanic" 

train_data_key = f"{read_prefix}/train.csv"
test_data_key = f"{read_prefix}/test.csv"
model_key = f"{write_prefix}/model"
output_key = f"{write_prefix}/output"

train_data_uri = f"s3://{read_bucket}/{train_data_key}"
test_data_uri = f"s3://{read_bucket}/{test_data_key}"

print(train_data_uri)

train_df = pd.read_csv(train_data_uri)
test_df = pd.read_csv(test_data_uri)
print(train_df.head())



def train(train_df, test_df):
    y = train_df["Survived"]

    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X = pd.get_dummies(train_df[features])
    X_test = pd.get_dummies(test_df[features])

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(X, y)

    return model

def upload_model(model):
    with open("./Randomforest-model", "wb") as f:
        joblib.dump(model, f)    
    

    model_location = model_key + "/Randomforest-model"
    s3_client.upload_file(Filename="./Randomforest-model", Bucket=write_bucket, Key=model_location)

model = train(train_df, test_df)
upload_model(model)
