import requests
import pandas as pd
from datetime import datetime, timedelta

def get_nasa_features(lat, lon):

    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={start}&end={end}"
        "&parameters=T2M_MAX,T2M_MIN,PRECTOT,ALLSKY_SFC_SW_DWN"
        "&community=ag"
        f"&latitude={lat}&longitude={lon}"
        "&format=JSON"
    )

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            print("NASA HTTP ERROR:", response.status_code)
            return None

        data = response.json()
        params = data["properties"]["parameter"]

        # 🔥 Safely get parameters (avoid KeyError)
        tmax = params.get("T2M_MAX", {})
        tmin = params.get("T2M_MIN", {})
        prectot = params.get("PRECTOT", {})
        radiation = params.get("ALLSKY_SFC_SW_DWN", {})

        # Ensure temperature exists
        if not tmax or not tmin:
            print("Temperature data missing")
            return None

        dates = list(tmax.keys())

        df = pd.DataFrame({
            "date": dates,
            "T2M_MAX": [tmax.get(d, 0) for d in dates],
            "T2M_MIN": [tmin.get(d, 0) for d in dates],
            "PRECTOT": [prectot.get(d, 0) for d in dates],
            "ALLSKY_SFC_SW_DWN": [radiation.get(d, 0) for d in dates],
        })

        df["temperature"] = (df["T2M_MAX"] + df["T2M_MIN"]) / 2

        return df

    except Exception as e:
        print("NASA EXCEPTION:", e)
        return None
