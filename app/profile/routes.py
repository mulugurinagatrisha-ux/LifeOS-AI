from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.profile import profile
from app.profile.forms import (
    ProfileForm,
    ChangePasswordForm
)

from app.profile.utils import save_profile_picture
from app.extensions import db
from app.models import User


@profile.route("/")
@login_required
def view_profile():

    return render_template(
        "profile/profile.html",
        user=current_user
    )


@profile.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = ProfileForm()

    if form.validate_on_submit():

        # Check duplicate email
        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user and existing_user.id != current_user.id:
            flash(
                "Email already exists.",
                "danger"
            )
            return redirect(
                url_for("profile.edit_profile")
            )

        current_user.full_name = form.full_name.data.strip()
        current_user.email = form.email.data.strip().lower()
        current_user.phone = form.phone.data.strip() if form.phone.data else None
        current_user.bio = form.bio.data.strip() if form.bio.data else None
        current_user.gender = form.gender.data

        if form.profile_image.data:
            filename = save_profile_picture(
                form.profile_image.data
            )

            if filename:
                current_user.profile_image = filename

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("profile.view_profile")
        )

    if request.method == "GET":

       form.full_name.data = current_user.full_name
       form.email.data = current_user.email
       form.phone.data = current_user.phone
       form.gender.data = current_user.gender
       form.bio.data = current_user.bio 

    return render_template(
        "profile/edit_profile.html",
        form=form
    )


@profile.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not check_password_hash(
            current_user.password,
            form.current_password.data
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("profile.change_password")
            )

        current_user.password = generate_password_hash(
            form.new_password.data
        )

        db.session.commit()

        flash(
            "Password changed successfully.",
            "success"
        )

        return redirect(
            url_for("profile.view_profile")
        )

    return render_template(
        "profile/change_password.html",
        form=form
    )