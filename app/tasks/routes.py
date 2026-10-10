from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .import tasks
from .forms import TaskForm
from app.extensions import db
from app.models import Task,Goal
from app.ai_goals.models import AIGoal


@tasks.route("/")
@login_required
def all_tasks():

    tasks_list = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Task.created_at.desc()
    ).all()

    return render_template(
        "tasks/index.html",
        tasks=tasks_list
    )
@tasks.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task Added Successfully!")

        return redirect(url_for("tasks.all_tasks"))

    return render_template(
        "tasks/add_task.html",
        form=form
    )
@tasks.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    form = TaskForm(obj=task)

    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data

        db.session.commit()

        flash("Task Updated Successfully!")

        return redirect(url_for("tasks.all_tasks"))

    return render_template(
        "tasks/edit_task.html",
        form=form
    )


@tasks.route("/delete/<int:id>")
@login_required
def delete_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Task Deleted Successfully!")

    return redirect(url_for("tasks.all_tasks"))

@tasks.route("/toggle/<int:id>")
@login_required
def toggle_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    # Toggle completion
    task.completed = not task.completed

    db.session.commit()

    if task.completed:
        flash(
            "Task marked as completed!",
            "success"
        )
    else:
        flash(
            "Task marked as pending!",
            "info"
        )

    return redirect(url_for("tasks.all_tasks"))