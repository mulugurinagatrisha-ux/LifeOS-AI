from flask import render_template, request, jsonify
from flask_login import login_required
from . import weather
from .services import get_current_weather, get_forecast
from app.utils.weather import get_hourly_forecast

@weather.route("/")
@login_required
def home():
    return render_template("weather/index.html")


@weather.route("/api", methods=["POST"])
@login_required
def weather_api():

    try:

        data = request.get_json()

        lat = data.get("lat")
        lon = data.get("lon")

        weather = get_current_weather(lat, lon)

        if weather is None:

            return jsonify({
                "success": False
            })

        return jsonify({
            "success": True,
            "weather": weather
        })

    except Exception as e:

        print(e)

        return jsonify({
            "success": False,
            "message": str(e)
        })
@weather.route("/forecast", methods=["POST"])
@login_required
def forecast_api():

    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")

    forecast = get_forecast(lat, lon)

    return jsonify({
        "forecast": forecast
    })  
@weather.route("/hourly", methods=["POST"])
@login_required
def hourly():

    data = request.get_json()

    hourly = get_hourly_forecast(
        data["lat"],
        data["lon"]
    )

    return jsonify({

        "success": True,

        "hourly": hourly

    })          