from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    SubmitField
)

from wtforms.validators import DataRequired


class GoalForm(FlaskForm):

    title = StringField(
        "Goal Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    target_date = DateField(
        "Target Date",
        format="%Y-%m-%d"
    )

    submit = SubmitField(
        "Save Goal"
    )