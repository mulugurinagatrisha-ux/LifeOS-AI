from datetime import datetime
from app.extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(20))

    bio = db.Column(db.Text)

    gender = db.Column(db.String(20))

    profile_image = db.Column(
        db.String(200),
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    notes = db.relationship(
        "Note",
        backref="user",
        lazy=True
    )

    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True
    )

    goals = db.relationship(
        "Goal",
        backref="user",
        lazy=True
    )

    expenses = db.relationship(
        "Expense",
        backref="user",
        lazy=True
    )

    habits = db.relationship(
        "Habit",
        backref="user",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.email}>"