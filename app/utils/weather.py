import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

print("=" * 50)
print("OPENWEATHER_API_KEY =", API_KEY)
print("=" * 50)


def get_weather(lat, lon):
    print("\n========== WEATHER REQUEST ==========")
    print("Latitude :", lat)
    print("Longitude:", lon)

    if not API_KEY:
        print("❌ OPENWEATHER_API_KEY not found!")
        return None

    if lat is None or lon is None:
        print("❌ Latitude or Longitude is missing!")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        print("\nRequest URL:")
        print(response.url)

        print("\nStatus Code:", response.status_code)

        if response.status_code != 200:
            print("Response:")
            print(response.text)
            return None

        data = response.json()

        weather = {
            "temp": round(data["main"]["temp"]),
            "city": data["name"],
            "country": data["sys"]["country"],
            "icon": data["weather"][0]["icon"],
            "desc": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        }

        print("\nWeather Data:")
        print(weather)

        return weather

    except requests.exceptions.RequestException as e:
        print("❌ Network Error:", e)
        return None

    except Exception as e:
        print("❌ Error:", e)
        return None
def get_hourly_forecast(lat, lon):

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

    hourly = []

    # Next 8 entries (3 hours each = 24 hours)

    for item in data["list"][:8]:

        hourly.append({

            "time": item["dt_txt"].split()[1][:5],

            "temp": round(item["main"]["temp"]),

            "icon": item["weather"][0]["icon"]

        })

    return hourly    