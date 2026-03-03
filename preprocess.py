
import pandas as pd

def preprocess_weather(df):
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df
