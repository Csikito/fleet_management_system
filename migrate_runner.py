from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

import configparser

ini = configparser.ConfigParser()
ini.read(".fleet.ini")

db = SQLAlchemy()
migrate = Migrate()

def create_migration_app():
    app = Flask(__name__)
    app.config.from_object(Config("FLEET"))
    db.init_app(app)
    migrate.init_app(app, db)

    return app

app = create_migration_app()
