from flask import Blueprint, render_template
from flask_login import current_user, login_required

admin_page = Blueprint("dashboard", __name__)


@admin_page.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html",
                           name = current_user.first_name)
