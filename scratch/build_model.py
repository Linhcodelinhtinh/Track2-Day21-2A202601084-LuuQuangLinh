import pandas as pd
import joblib
import boto3
import os
from sklearn.ensemble import GradientBoostingClassifier

df_train = pd.read_csv("data/train_batch1.csv")
X_train = df_train.drop(columns=["target"])
y_train = df_train["target"]

model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.joblib")

s3 = boto3.client("s3")
s3.upload_file("models/model.joblib", "luuquanglinh-dvc-bucket", "artifacts/current/model.joblib")
print("Model created and uploaded to S3 successfully!")
