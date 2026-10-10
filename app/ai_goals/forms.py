from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired


class AIGoalForm(FlaskForm):

    goal = StringField(
        "Goal",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Weight Loss","Weight Loss"),
            ("Weight Gain","Weight Gain"),
            ("Muscle Building","Muscle Building"),
            ("Fitness","Fitness"),
            ("Running","Running"),
            ("Cycling","Cycling"),
            ("Yoga","Yoga"),
            ("Diet","Diet"),
            ("Study","Study"),
            ("Career","Career"),
            ("Savings","Savings"),
            ("Productivity","Productivity"),
            ("Other","Other")
        ]
    )

    current_value = StringField(
        "Current Value"
    )

    target_value = StringField(
        "Target Value"
    )

    notes = TextAreaField(
        "Additional Notes"
    )

    submit = SubmitField(
        "🤖 Generate AI Plan"
    )