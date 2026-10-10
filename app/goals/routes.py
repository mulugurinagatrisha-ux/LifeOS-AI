from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from flask import request
from flask_login import (
    login_required,
    current_user
)

from app.goals import goals
from app.extensions import db
from app.models import Goal
from app.goals.forms import GoalForm


@goals.route("/")
@login_required
def all_goals():

    goals_list = Goal.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "goals/goals.html",
        goals=goals_list
    )


@goals.route("/add", methods=["GET", "POST"])
@login_required
def add_goal():

    form = GoalForm()

    if form.validate_on_submit():

        goal = Goal(
            title=form.title.data,
            description=form.description.data,
            target_date=form.target_date.data,
            user_id=current_user.id
        )

        db.session.add(goal)
        db.session.commit()

        flash(
            "Goal Added Successfully!",
            "success"
        )

        return redirect(
            url_for("goals.all_goals")
        )

    return render_template(
        "goals/add_goal.html",
        form=form
    )
@goals.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_goal(id):

    goal = Goal.query.get_or_404(id)

    if goal.user_id != current_user.id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("goals.all_goals"))

    form = GoalForm(obj=goal)

    if form.validate_on_submit():

        goal.title = form.title.data
        goal.description = form.description.data
        goal.target_date = form.target_date.data

        db.session.commit()

        flash("Goal Updated Successfully!", "success")

        return redirect(url_for("goals.all_goals"))

    return render_template(
        "goals/edit_goal.html",
        form=form
    )    
@goals.route("/delete/<int:id>")
@login_required
def delete_goal(id):

    goal = Goal.query.get_or_404(id)

    if goal.user_id != current_user.id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("goals.all_goals"))

    db.session.delete(goal)
    db.session.commit()

    flash("Goal Deleted Successfully!", "success")

    return redirect(url_for("goals.all_goals"))
@goals.route("/toggle/<int:id>")
@login_required
def toggle_goal(id):

    goal = Goal.query.get_or_404(id)

    if goal.user_id != current_user.id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("goals.all_goals"))

    goal.completed = not goal.completed

    db.session.commit()

    return redirect(url_for("goals.all_goals")) 
   