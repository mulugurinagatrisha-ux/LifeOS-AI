from app.extensions import db


class Chat(db.Model):

    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)

    question = db.Column(db.Text, nullable=False)

    answer = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_sessions.id")
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )