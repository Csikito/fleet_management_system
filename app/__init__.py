from flask_migrate import Migrate

from config import Config, TestConfig, ini
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .models import User, PermissionStatusCodes
from .permissions_helper import has_permission

def create_app(flask_app, test=False):
    app = Flask(__name__)

    if test:
        config = TestConfig(flask_app)
    else:
        config = Config(flask_app)
    app.port = ini[flask_app]["port"]
    app.config.from_object(config)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    app.jinja_env.globals["has_permission"] = has_permission
    app.jinja_env.globals["PermissionStatusCodes"] = PermissionStatusCodes

    if flask_app == "FLEET":
        login_manager.init_app(app)
        login_manager.login_view = "login_page.login"
        app.config['REMEMBER_COOKIE_DURATION'] = 60 * 60 * 24 * 7  # 7 day
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # e.g update img


        @login_manager.user_loader
        def load_user(user_id):
            user = User.query.get(int(user_id))
            return user

        with app.app_context():
            from .routes import auth, dashboard
            from .util import page_not_found, page_internal_server_error , page_no_access
            from .init_admin import create_admin_user

            create_admin_user()
            app.register_blueprint(auth.login_page)
            app.register_blueprint(dashboard.admin_page)
            app.register_error_handler(403, page_no_access)
            app.register_error_handler(404, page_not_found)
            app.register_error_handler(500, page_internal_server_error)

    return app
