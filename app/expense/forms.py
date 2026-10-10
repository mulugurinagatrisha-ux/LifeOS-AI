from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    FloatField,
    TextAreaField,
    SubmitField,
    SelectField
)

from wtforms.validators import (
    DataRequired,
    NumberRange,
    Optional
)


class ExpenseForm(FlaskForm):

    title = StringField(
        "Expense Title",
        validators=[DataRequired()]
    )

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Shopping", "Shopping"),
            ("Bills", "Bills"),
            ("Education", "Education"),
            ("Medical", "Medical"),
            ("Entertainment", "Entertainment"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()]
    )

    submit = SubmitField("Save Expense")