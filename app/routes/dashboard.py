import json

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_required
from ..decorators import register_breadcrumbs, permission_required, get_breadcrumbs, permission_required
from ..models import User, Permission, PermissionStatusCodes
from ..forms import PermissionForm


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
@permission_required(PermissionStatusCodes.USERS)
def users():
    return render_template("dashboard.html",
                           name = current_user.first_name,
                           header_title="Users"
                           )


@admin_page.route('/permission', methods=["GET"])
@register_breadcrumbs(admin_page, ".permission", "Permission ")
@permission_required(PermissionStatusCodes.PERMISSION)
def permission():
    return render_template("permission_table.html",
                           header_title="Permission",
                           )


@admin_page.route('/server_side_permission', methods=["GET"])
@register_breadcrumbs(admin_page, ".permission", "Permission ")
@permission_required(PermissionStatusCodes.PERMISSION)
def server_side_permission():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    query = Permission.query.offset(start).limit(length)
    total_records = Permission.query.count()

    data = [{"id": perm.id, "name": perm.name, "permissions": perm.get_processed_permissions()} for perm in query]
    return jsonify({
        "draw": request.args.get('draw', 1),
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })



@admin_page.route('/permission_edit/<int:id>', methods=["GET", "POST"])
@register_breadcrumbs(admin_page, ".permission_edit.id", "Permission edit ")
def permission_edit(id):
    if id == 0:
        permission = Permission()
    else:
        permission = Permission.query.get_or_404(id)
    form = PermissionForm(formdata=request.form)

    if request.method == "POST" and form.validate_on_submit():
        permission.name = form.name.data
        selected_permissions = [int(id) for id, field in form.boolean_fields if field.data ]
        permission.permissions = json.dumps(selected_permissions)
        permission.save()
        flash('Permission updated successfully.', 'success')
        return redirect(url_for('dashboard.permission'))
    else:
        form.name.data = permission.name
        existing_permissions = json.loads(permission.permissions) if permission.permissions else []
        for id, field in form.boolean_fields:
            if id in existing_permissions:
                field.data = True

    return render_template("permission_edit.html",
                           header_title="Permission Edit",
                           form=form)
