import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        print("API ERROR:", response.text)
        return None

    data = response.json()

    records = []

    for item in data["list"]:
        records.append({
            "date": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "humidity": item["main"]["humidity"]
        })

    df = pd.DataFrame(records)

    return df
