from flask import Blueprint

ai_goals = Blueprint(
    "ai_goals",
    __name__,
    template_folder="templates"
)

from app.ai_goals import routes