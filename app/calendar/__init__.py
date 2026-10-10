from flask import Blueprint

calendar = Blueprint(
    "calendar",
    __name__,
    url_prefix="/calendar"
)

from app.calendar import routes