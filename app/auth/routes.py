from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import auth
from app.auth.forms import RegisterForm, LoginForm
from app.extensions import db, bcrypt
from app.models import User


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash("Email already exists.")
            return render_template(
                "auth/register.html",
                form=form
            )

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful. Please Login.")

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Login Successful.")

            return redirect(url_for("dashboard.home"))

        flash("Invalid Email or Password.")

    return render_template(
        "auth/login.html",
        form=form
    )


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully.")

    return redirect(url_for("auth.login"))