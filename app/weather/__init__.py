from flask import Blueprint

weather = Blueprint(
    "weather",
    __name__,
    template_folder="templates"
)

from app.weather import routes