import json
from enum import unique

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .util import get_permission_status_name

class MyDbModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class PermissionStatusCodes:
    # Sidebar
    USERS = 1
    PERMISSION = 2
    VEHICLES = 3
    FINANCIAL_REPORT = 4
    VEHICLE_REPORT = 5
    MILEAGE_REPORT = 6


class Permission(db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    permissions = db.Column(db.Text(), nullable=True)

    def get_processed_permissions(self):
        permission_ids = json.loads(self.permissions) if self.permissions else []
        names = [get_permission_status_name(True).get(perm_id, f"Unknown ({perm_id})") for perm_id in permission_ids]
        return ", ".join(names)


class User(UserMixin, db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    image = db.Column(db.LargeBinary())
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    permission = db.Column(db.Integer(), db.ForeignKey(Permission.id), nullable=True)
    permissions = db.relationship(Permission, foreign_keys=[permission])
    active = db.Column(db.Boolean())

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)
