from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, migrate, bcrypt
from app.profile import profile
from app.auth import auth
from app.dashboard import dashboard
from app.notes import notes
from app.tasks import tasks
from app.ai import ai
from app.calendar import calendar
from app.goals import goals
from app.expense import expense
from app.models import User
from app.weather import weather
from app.ai_goals import ai_goals


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(notes)
    app.register_blueprint(tasks)
    app.register_blueprint(ai)
    app.register_blueprint(calendar)
    app.register_blueprint(goals)
    app.register_blueprint(profile)
    app.register_blueprint(
    expense,
    url_prefix="/expense"
)
    app.register_blueprint(
    weather,
    url_prefix="/weather"
)
    app.register_blueprint(
    ai_goals,
    url_prefix="/ai_goals"
)
    
    
    return app