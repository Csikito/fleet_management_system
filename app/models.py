from enum import unique

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class MyDbModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserRight(UserMixin, db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    app_right = db.Column(db.Text(), nullable=True)


class User(UserMixin, db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    image = db.Column(db.LargeBinary())
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    app_right = db.Column(db.Integer(), db.ForeignKey(UserRight.id), nullable=True)
    user_right = db.relationship(UserRight, foreign_keys=[app_right])
    active = db.Column(db.Boolean())

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)
