from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    FileField,
    SubmitField,
    SelectField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    Optional
)


class ProfileForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            Optional(),
            Length(max=20)
        ]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("", "Select Gender"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ],
        validators=[Optional()]
    )

    bio = TextAreaField(
        "Bio",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    profile_image = FileField(
        "Profile Picture"
    )

    submit = SubmitField(
        "Update Profile"
    )


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired()
        ]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("new_password")
        ]
    )

    submit = SubmitField(
        "Change Password"
    )