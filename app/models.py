from flask_login import UserMixin
from app.extensions import db
from app.models import Task, Goal
# ==========================
# GOALS
# ==========================

class Goal(db.Model):

    __tablename__ = "goals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    goal = db.Column(
        db.String(200),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    category = db.Column(
        db.String(100),
        nullable=True
    )

    target_date = db.Column(
        db.Date,
        nullable=True
    )

    progress = db.Column(
        db.Integer,
        default=0
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    tasks = db.relationship(
        "Task",
        backref="goal",
        lazy=True
    )

# ==========================
# USER
# ==========================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    gender = db.Column(
        db.String(20),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    profile_image = db.Column(
        db.String(255),
        nullable=False,
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationships

    notes = db.relationship(
        "Note",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    expenses = db.relationship(
        "Expense",

        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"


# ==========================
# NOTES
# ==========================

class Note(db.Model):

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# ==========================
# TASKS
# ==========================

class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    goal_id = db.Column(
    db.Integer,
    db.ForeignKey("goals.id"),
    nullable=True
)    
# ==========================
# EXPENSES
# ==========================
class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(120),
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    category = db.Column(
        db.String(50),
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    def __repr__(self):
        return f"<Expense {self.title}>"