import argparse
import joblib
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


# inference functions ---------------
def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf


if __name__ == "__main__":
    print("extracting arguments")
    parser = argparse.ArgumentParser()

    parser.add_argument("--n-estimators", type=int, default=10)

    # Data, model, and output directories
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train-dir", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test-dir", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    parser.add_argument("--train-file", type=str, default="train.csv")
    parser.add_argument(
        "--features", type=str
    )
    parser.add_argument(
        "--target", type=str
    )

    args, _ = parser.parse_known_args()

    print("reading data")
    train_df = pd.read_csv(os.path.join(args.train_dir, args.train_file))

    print("building training and testing datasets")
    X_train = pd.get_dummies(train_df[args.features.split()])
    y_train = train_df[args.target]

    # train
    print("training model")
    model = RandomForestClassifier(
        n_estimators=args.n_estimators, max_depth=5, random_state=1
    )

    model.fit(X_train, y_train)

    # persist model
    path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, path)
    print("model persisted at " + path)
