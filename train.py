import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Load dataset (cumulative_gdd, humidity, ndvi, PRECTOT, ALLSKY_SFC_SW_DWN, pest, outbreak)
df = pd.read_csv("data/sample_dataset.csv")

# Encode pest
le = LabelEncoder()
df["pest_encoded"] = le.fit_transform(df["pest"])

# Features & labels
X = df[["cumulative_gdd", "humidity", "ndvi", "PRECTOT", "ALLSKY_SFC_SW_DWN", "pest_encoded"]]
y = df["outbreak"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/multi_pest_model.pkl")
print("Multi-pest model trained and saved.")

# Evaluate
preds = model.predict(X_test)
print(classification_report(y_test, preds))
