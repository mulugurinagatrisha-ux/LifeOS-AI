from flask import Blueprint

expense = Blueprint(
    "expense",
    __name__,
    template_folder="../templates/expense"
)

from app.expense import routes