from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import DataRequired


class TaskForm(FlaskForm):

    title = StringField(
        "Task Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low")
        ]
    )

    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d"
    )

    submit = SubmitField("Save Task")