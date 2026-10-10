from datetime import datetime

from app.extensions import db


class AIGoal(db.Model):

    __tablename__ = "ai_goals"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    goal = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    current_value = db.Column(
        db.Integer,
        default=0
    )

    target_value = db.Column(
        db.Integer,
        default=0
    )

    estimated_days = db.Column(
        db.Integer,
        default=0
    )

    progress = db.Column(
        db.Float,
        default=0
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    daily_tasks = db.Column(
        db.Text
    )

    weekly_goal = db.Column(
        db.Text
    )

    diet_plan = db.Column(
        db.Text
    )

    water_intake = db.Column(
        db.String(100)
    )

    workout_plan = db.Column(
        db.Text
    )

    motivation = db.Column(
        db.Text
    )

    ai_response = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )