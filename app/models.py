import json
import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import cast, Float

from flask_login import UserMixin
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
    TRANSPORT = 4
    VEHICLE_REPORT = 5
    TRANSPORT_REPORT = 6


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
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


class VehicleTypeStatusCodes:
    CAR = 1
    VAN = 2
    TRUCK = 3


class VehicleModelStatusCodes:
    CITROEN_JUMPER = 1
    OPEL_MOVANO = 2
    SCANIA_R450 = 3
    MAN_TGX = 4
    OPEL_ASTRA = 5
    SEAT_IBIZA = 6


class Vehicle(db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.Integer, nullable=False)
    model = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    engine_type = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary())
    initial_mileage = db.Column(db.Integer, nullable=False)
    current_mileage = db.Column(db.Integer, nullable=True)
    registration_expiry_date = db.Column(db.Date, nullable=True)
    driver = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=True)
    user = db.relationship(User, foreign_keys=[driver])


class Cargo:
    GRAIN = 1
    IRON = 2
    OTHER = 3


class Transport(db.Model, MyDbModel):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=True)
    cargo = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    delivered_by = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=True)
    user = db.relationship(User, foreign_keys=[delivered_by])

    @hybrid_property
    def total_fee(self):
        return self.amount * self.unit_price

    @total_fee.expression
    def total_fee(cls):
        return cast(cls.amount, Float) * cast(cls.unit_price, Float)
