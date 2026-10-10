from app.extensions import db


class ChatSession(db.Model):

    __tablename__ = "chat_sessions"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False,
        default="New Chat"
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

    chats = db.relationship(
        "Chat",
        backref="session",
        lazy=True,
        cascade="all, delete-orphan"
    )