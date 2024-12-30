from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from ..decorators import register_breadcrumbs, get_breadcrumbs


admin_page = Blueprint("dashboard", __name__)

@admin_page.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.dashboard'))


@admin_page.route('/dashboard', methods=["GET"])
@login_required
@register_breadcrumbs(admin_page, ".dashboard", "Dashboard")
def dashboard():
    return render_template("dashboard.html",
                           name = current_user.first_name,
                           header_title="Dashboard"
                           )
