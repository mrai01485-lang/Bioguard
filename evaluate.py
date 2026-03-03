import pandas as pd
import joblib
from sklearn.metrics import classification_report

def evaluate_model():
    df = pd.read_csv("data/sample_dataset.csv")
    model = joblib.load("models/pest_model.pkl")

    X = df[["cumulative_gdd", "humidity", "ndvi"]]
    y = df["outbreak"]

    predictions = model.predict(X)

    print(classification_report(y, predictions))
