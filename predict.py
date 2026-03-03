import joblib
from settings import MODEL_PATH

def predict_outbreak_risk(cumulative_gdd, humidity, ndvi):
    model = joblib.load(MODEL_PATH)

    features = [[cumulative_gdd, humidity, ndvi]]
    prob = model.predict_proba(features)[0][1]

    return prob
