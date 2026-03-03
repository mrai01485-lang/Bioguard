import streamlit as st
import joblib
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from sklearn.preprocessing import LabelEncoder

from nasa_fetcher import get_nasa_features
from gdd_calculator import calculate_gdd_series
from lifecycle_model import predict_stage
from ndvi_fetcher import get_ndvi_value
from advice import get_advice
from translator import translate_text
from risk_engine import get_control_methods, recommend_method, generate_extended_advisory
import plots


st.set_page_config(page_title="BioGuard AI", layout="wide")
st.title("🌾 BioGuard AI - Multi-Pest Prediction & Control System")

# ----------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------
try:
    model = joblib.load("models/multi_pest_model.pkl")
except:
    st.error("Model file not found. Train the model first.")
    st.stop()

# ----------------------------------------------------
# SIDEBAR INPUTS
# ----------------------------------------------------
st.sidebar.header("Farmer Inputs")

city = st.sidebar.text_input("Enter City Name")
budget = st.sidebar.slider("Available Budget (₹)", 500, 5000, 2000)

language = st.sidebar.selectbox(
    "Select Language",
    ["en", "hi", "mr", "ta", "te", "bn"]
)

pest = st.sidebar.selectbox(
    "Select Pest",
    ["Armyworm", "Stem Borer", "Aphids", "Whitefly", "Thrips"]
)

analyze = st.sidebar.button("Analyze")

# ----------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------
if analyze:

    if not city:
        st.warning("Please enter a city.")
        st.stop()

    # ---------------- GEOLOCATION -------------------
    geolocator = Nominatim(user_agent="bioguard_ai")
    location = geolocator.geocode(city)

    if not location:
        st.error("City not found.")
        st.stop()

    lat = location.latitude
    lon = location.longitude

    # ---------------- NASA DATA ---------------------
    df = get_nasa_features(lat, lon)

    if df is None:
        st.error("NASA API fetch failed.")
        st.stop()

    # ---------------- PREPROCESS --------------------
    df = calculate_gdd_series(df)

    cumulative_gdd = df["cumulative_gdd"].iloc[-1]
    avg_rainfall = df["PRECTOT"].mean()
    avg_radiation = df["ALLSKY_SFC_SW_DWN"].mean()
    avg_temp = df["temperature"].mean()
    humidity = 65  # temporary fixed value unless you integrate humidity API
    ndvi = get_ndvi_value()

    # ---------------- PEST ENCODING -----------------
    pests = ["Armyworm", "Stem Borer", "Aphids", "Whitefly", "Thrips"]
    le = LabelEncoder()
    le.fit(pests)
    pest_encoded = le.transform([pest])[0]

    # ---------------- ML FEATURES -------------------
    features = np.array([[
        cumulative_gdd,
        humidity,
        ndvi,
        avg_rainfall,
        avg_radiation,
        pest_encoded
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    risk_score = float(probability)

    if risk_score < 0.4:
        risk_level = "Low"
    elif risk_score < 0.7:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    # ---------------- DISPLAY METRICS ---------------
    col1, col2 = st.columns(2)
    col1.metric("Outbreak Probability", f"{risk_score:.2f}")
    col2.metric("Risk Level", risk_level)

    # ---------------- LIFE CYCLE --------------------
    stage = predict_stage(cumulative_gdd)
    st.info(f"Predicted Pest Life Stage: {stage}")

    # ---------------- RISK GRAPH --------------------
    st.subheader("Pest Risk Trend")
    df["GDD"] = df["cumulative_gdd"]
    fig1 = plots.pest_risk_time_series(df, risk_score)
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- CONTROL METHODS ---------------
    methods_df = get_control_methods()
    affordable = methods_df[methods_df["cost"] <= budget]

    st.subheader("Available Control Methods")
    st.dataframe(affordable)

    st.plotly_chart(plots.cost_effectiveness_plot(methods_df), use_container_width=True)
    st.plotly_chart(plots.risk_heatmap(methods_df), use_container_width=True)
    st.plotly_chart(plots.yield_gain_plot(methods_df), use_container_width=True)

    # ---------------- RECOMMENDATION ----------------
    if not affordable.empty:
        if risk_level == "High":
            best = affordable.sort_values("effectiveness", ascending=False).iloc[0]
        else:
            best = affordable.sort_values("risk").iloc[0]

        st.subheader("Recommended Strategy")
        st.success(
            f"""
            Method: {best['name']}
            Cost: ₹{best['cost']}
            Effectiveness: {best['effectiveness']*100:.0f}%
            Environmental Impact: {best['environmental_impact']}
            """
        )
    else:
        st.error("No method within selected budget.")

    # ---------------- ADVISORY ----------------------
    advice_text = get_advice(
        pest=pest,
        risk=risk_level,
        rainfall=avg_rainfall,
        radiation=avg_radiation,
        temperature=avg_temp
    )

    translated = translate_text(advice_text, language)

    st.subheader("Farmer Advisory")
    st.write(translated)

    # ---------------- ENV SUMMARY -------------------
    st.subheader("Environmental Summary")
    st.write(f"Cumulative GDD: {round(cumulative_gdd,2)}")
    st.write(f"Average Rainfall: {round(avg_rainfall,2)} mm")
    st.write(f"Average Radiation: {round(avg_radiation,2)} W/m²")
    st.write(f"NDVI: {ndvi}")
