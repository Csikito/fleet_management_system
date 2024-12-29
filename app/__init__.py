from config import Config, TestConfig, ini
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(flask_app, test=False):
    app = Flask(__name__)

    if test:
        config = TestConfig()
    else:
        config = Config()
    app.port = ini[flask_app]["port"]
    app.config.from_object(config)
    app.config.from_object(config)

    db.init_app(app)

    if flask_app == "FLEET":
        # login_manager.init_app(app)
        from .routes import auth, dashboard, vehicles, users

        app.register_blueprint(dashboard.bp)
        # app.register_blueprint(auth.bp)
        # app.register_blueprint(vehicles.bp)
        # app.register_blueprint(users.bp)

    return app
