from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    description = TextAreaField("Description")

    event_date = DateField(
        "Date",
        validators=[DataRequired()]
    )

    event_time = TimeField("Time")

    submit = SubmitField("Save Event")