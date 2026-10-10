from app.extensions import db


class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    event_date = db.Column(db.Date, nullable=False)

    event_time = db.Column(db.Time)

    color = db.Column(db.String(20), default="#4f46e5")

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Event {self.title}>"