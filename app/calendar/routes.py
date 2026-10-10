from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from datetime import date

from app.extensions import db
from app.calendar import calendar
from app.calendar.forms import EventForm
from app.calendar.models import Event


@calendar.route("/")
@login_required
def index():

    events = Event.query.filter_by(
        user_id=current_user.id
    ).order_by(Event.event_date).all()

    today_events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.event_date == date.today()
    ).all()

    upcoming_events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.event_date > date.today()
    ).order_by(Event.event_date).all()

    return render_template(
        "calendar/calendar.html",
        events=events,
        today_events=today_events,
        upcoming_events=upcoming_events
    )


@calendar.route("/add", methods=["GET", "POST"])
@login_required
def add_event():

    form = EventForm()

    if form.validate_on_submit():

        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            user_id=current_user.id
        )

        db.session.add(event)
        db.session.commit()

        flash("Event Added Successfully", "success")

        return redirect(url_for("calendar.index"))

    return render_template(
        "calendar/add_event.html",
        form=form
    )


@calendar.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):

    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash("Access Denied", "danger")
        return redirect(url_for("calendar.index"))

    form = EventForm(obj=event)

    if form.validate_on_submit():

        event.title = form.title.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.event_time = form.event_time.data

        db.session.commit()

        flash("Event Updated Successfully", "success")

        return redirect(url_for("calendar.index"))

    return render_template(
        "calendar/edit_event.html",
        form=form
    )


@calendar.route("/delete/<int:event_id>")
@login_required
def delete_event(event_id):

    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash("Access Denied", "danger")
        return redirect(url_for("calendar.index"))

    db.session.delete(event)
    db.session.commit()

    flash("Event Deleted Successfully", "success")

    return redirect(url_for("calendar.index"))
@calendar.route("/month")
@login_required
def month_calendar():

    events = Event.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "calendar/month_calendar.html",
        events=events
    )