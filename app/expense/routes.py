from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from app.models import Expense
from app.expense import expense
from app.expense.forms import ExpenseForm


@expense.route("/")
@login_required
def all_expenses():

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Expense.created_at.desc()
    ).all()

    total = sum(e.amount for e in expenses)

    return render_template(
        "expense/index.html",
        expenses=expenses,
        total=total
    )
@expense.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense_data = Expense(
            title=form.title.data,
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )

        db.session.add(expense_data)
        db.session.commit()

        flash(
            "Expense Added Successfully",
            "success"
        )

        return redirect(
            url_for("expense.all_expenses")
        )

    return render_template(
        "expense/add.html",
        form=form
    )
@expense.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_expense(id):

    expense_data = Expense.query.get_or_404(id)

    if expense_data.user_id != current_user.id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("expense.all_expenses"))

    form = ExpenseForm()

    if form.validate_on_submit():

        expense_data.title = form.title.data
        expense_data.amount = form.amount.data
        expense_data.category = form.category.data
        expense_data.description = form.description.data

        db.session.commit()

        flash(
            "Expense Updated Successfully",
            "success"
        )

        return redirect(
            url_for("expense.all_expenses")
        )

    if form.errors == {}:

        form.title.data = expense_data.title
        form.amount.data = expense_data.amount
        form.category.data = expense_data.category
        form.description.data = expense_data.description

    return render_template(
        "expense/add.html",
        form=form
    )


@expense.route("/delete/<int:id>")
@login_required
def delete_expense(id):

    expense_data = Expense.query.get_or_404(id)

    if expense_data.user_id != current_user.id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("expense.all_expenses"))

    db.session.delete(expense_data)
    db.session.commit()

    flash(
        "Expense Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("expense.all_expenses")
    )    
    