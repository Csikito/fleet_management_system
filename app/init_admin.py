from app.models import User
from flask import current_app
from werkzeug.security import generate_password_hash

def create_admin_user():
    username = current_app.config["ADMIN_USERNAME"].decode("utf-8")
    password = current_app.config["ADMIN_PASSWORD"].decode("utf-8")

    if not User.query.filter_by(username=username).first():
        admin = User(first_name="Admin", last_name="", username=username,
                     password=generate_password_hash(password), active=True, is_admin=True)
        admin.save()
