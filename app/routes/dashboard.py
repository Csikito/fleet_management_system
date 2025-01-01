import json

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from ..decorators import register_breadcrumbs, permission_required, get_breadcrumbs , Permissions, permission_required
from ..models import User, Permission


admin_page = Blueprint("dashboard", __name__)


@admin_page.route('/coming_soon', methods=["GET"])
def coming_soon():
    return render_template("coming_soon.html")

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


@admin_page.route('/users', methods=["GET"])
@register_breadcrumbs(admin_page, ".users", "User")
@permission_required(Permissions.USERS)
def users():
    return render_template("dashboard.html",
                           name = current_user.first_name,
                           header_title="Users"
                           )


@admin_page.route('/permission', methods=["GET"])
@register_breadcrumbs(admin_page, ".permission", "Permission ")
@permission_required(Permissions.PERMISSION)
def permission():
    return render_template("dashboard.html",
                           name = current_user.first_name,
                           header_title="Permission"
                           )
