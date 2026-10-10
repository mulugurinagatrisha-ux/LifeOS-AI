from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import notes
from .forms import NoteForm
from app.extensions import db
from app.models import Note


@notes.route("/")
@login_required
def all_notes():

    notes_list = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Note.created_at.desc()
    ).all()

    return render_template(
        "notes/index.html",
        notes=notes_list
    )


@notes.route("/add", methods=["GET", "POST"])
@login_required
def add_note():

    form = NoteForm()

    if form.validate_on_submit():

        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )

        db.session.add(note)
        db.session.commit()

        flash("Note Added Successfully!")

        return redirect(url_for("notes.all_notes"))

    return render_template(
        "notes/add_note.html",
        form=form
    )
@notes.route("/delete/<int:id>")
@login_required
def delete_note(id):

    note = Note.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("Note Deleted Successfully!")

    return redirect(url_for("notes.all_notes"))


@notes.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_note(id):

    note = Note.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    form = NoteForm(obj=note)

    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash("Note Updated Successfully!")

        return redirect(url_for("notes.all_notes"))

    return render_template(
        "notes/edit_note.html",
        form=form
    )