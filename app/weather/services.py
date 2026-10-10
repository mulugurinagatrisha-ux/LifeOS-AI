import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_current_weather(lat, lon):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "pressure": data["main"]["pressure"],
        "visibility": data["visibility"] // 1000,
        "icon": data["weather"][0]["icon"],"feels_like": round(data["main"]["feels_like"]),
"pressure": data["main"]["pressure"],
"sunrise": data["sys"]["sunrise"],
"sunset": data["sys"]["sunset"],
"visibility": data["visibility"] // 1000,
"temp_min": round(data["main"]["temp_min"]),
"temp_max": round(data["main"]["temp_max"]),
        "description": data["weather"][0]["description"].title()
    }
def get_forecast(lat, lon):

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    forecast = []

    for item in data["list"]:

        # Only one record per day (12 PM)
        if "12:00:00" in item["dt_txt"]:

            day = datetime.strptime(
                item["dt_txt"],
                "%Y-%m-%d %H:%M:%S"
            ).strftime("%A")

            forecast.append({

                "date": day,

                "temp": round(item["main"]["temp"]),

                "icon": item["weather"][0]["icon"],

                "desc": item["weather"][0]["description"].title()

            })

            # We need only 5 days
            if len(forecast) == 5:
                break

    return forecast