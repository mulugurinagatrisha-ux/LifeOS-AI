from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):

    message = TextAreaField(
        "Ask AI",
        validators=[DataRequired()]
    )

    submit = SubmitField("Send")