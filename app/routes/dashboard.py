import json
import base64
import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import current_user, login_required
from ..decorators import register_breadcrumbs, permission_required, get_breadcrumbs, permission_required
from ..models import User, Permission, PermissionStatusCodes, Vehicle
from ..forms import PermissionForm, NewUserForm, EditUserForm, VehicleForm
from ..util import get_vehicle_type_status_name, get_vehicle_model_status_name
from ..reports import export_csv, export_pdf, export_xlsx


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
    closest_vehicle = Vehicle.query.filter(Vehicle.registration_expiry_date >= datetime.datetime.today()) \
        .order_by(Vehicle.registration_expiry_date.asc()) \
        .first()
    data= { "users": User.query.count(),
            "vehicles": Vehicle.query.count(),
            "upcoming_operation": closest_vehicle.registration_expiry_date if closest_vehicle else "-"
            }
    return render_template("dashboard.html",
                           data = data,
                           header_title="Dashboard"
                           )


@admin_page.route('/permission', methods=["GET"])
@register_breadcrumbs(admin_page, ".permission", "Permission ")
@permission_required(PermissionStatusCodes.PERMISSION)
def permission():
    return render_template("permission_table.html",
                           header_title="Permission",
                           )


@admin_page.route('/server_side_permission', methods=["GET"])
@permission_required(PermissionStatusCodes.PERMISSION)
def server_side_permission():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    draw = int(request.args.get('draw', 1))
    order_column_index = int(request.args.get('order_column', 1))
    order_dir = request.args.get('order_dir', 'asc')

    column_map = {
        0: Permission.id,
        1: Permission.name,
        2: Permission.permissions,
    }

    order_column = column_map.get(order_column_index, Permission.id)
    if order_dir == 'desc':
        order_column = order_column.desc()

    query = Permission.query.order_by(order_column).offset(start).limit(length)
    total_records = Permission.query.count()

    data = [{"id": perm.id, "name": perm.name, "permissions": perm.get_processed_permissions()} for perm in query]
    return jsonify({
        "draw": draw,
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
        for field_id, field in form.boolean_fields:
            if field_id in existing_permissions:
                field.data = True

    return render_template("permission_edit.html",
                           header_title="Permission Edit",
                           form=form,
                           id=id)


@admin_page.route('/permission_delete/<int:id>', methods=["GET", "POST"])
@register_breadcrumbs(admin_page, ".permission_delete.id", "Permission edit ")
def permission_delete(id):
    permission = Permission.query.get_or_404(id)
    permission.delete()
    flash('Permission delete successfully.', 'success')
    return redirect(url_for('dashboard.permission'))


@admin_page.route('/users', methods=["GET"])
@register_breadcrumbs(admin_page, ".users", "User")
@permission_required(PermissionStatusCodes.USERS)
def users():
    return render_template("user_table.html",
                           header_title="Users"
                           )


@admin_page.route('/server_side_user', methods=["GET"])
@permission_required(PermissionStatusCodes.PERMISSION)
def server_side_user():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    draw = int(request.args.get('draw', 1))
    order_column_index = int(request.args.get('order_column', 1))
    order_dir = request.args.get('order_dir', 'asc')

    column_map = {
        1: User.first_name,
        2: User.username,
        3: User.permissions,
    }
    order_column = column_map.get(order_column_index, User.first_name)
    if order_dir == 'desc':
        order_column = order_column.desc()

    query = User.query.order_by(order_column).offset(start).limit(length)
    total_records = User.query.count()

    data = [{"id":user.id, "image":base64.b64encode(user.image).decode('utf-8') if user.image else None,
             "name": f"{user.first_name} {user.last_name}", "username": user.username, "permission": user.permissions.name} for user in query]
    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })


@admin_page.route('/user_edit/<int:id>', methods=["GET", "POST"])
@register_breadcrumbs(admin_page, ".user_edit.id", "User edit ")
def user_edit(id):
    if id == 0:
        user = User()
        form = NewUserForm()
    else:
        user = User.query.get_or_404(id)
        form = EditUserForm(obj=user)

    if request.method == "POST" and form.validate_on_submit():
        if isinstance(form, NewUserForm):
            user.username = form.username.data
            user.set_password(form.password.data)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.active = form.active.data
        user.permission = form.permission.data
        if form.image.data and not isinstance(form.image.data, bytes):
            file = form.image.data
            file_data  = file.read()
            user.image = file_data
        user.save()
        flash('Create new user successfully.', 'success')
        return redirect(url_for('dashboard.users'))

    img_bytes = user.image  # bytes
    if not img_bytes:
        img_bytes = open(current_app.static_folder + "/images/profile_img.png", 'rb').read()
    img_string = base64.b64encode(img_bytes).decode("ascii")

    return render_template("user_edit.html",
                           header_title="User edit",
                           img_string=img_string,
                           form=form,
                           )


@admin_page.route('/vehicles', methods=["GET"])
@register_breadcrumbs(admin_page, ".vehicles", "Vehicles")
@permission_required(PermissionStatusCodes.VEHICLES)
def vehicles():
    return render_template("vehicle_table.html",
                           header_title="Vehicles"
                           )


@admin_page.route('/server_side_vehicle', methods=["GET"])
@permission_required(PermissionStatusCodes.VEHICLES)
def server_side_vehicle():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    draw = int(request.args.get('draw', 1))
    order_column_index = int(request.args.get('order_column', 1))
    order_dir = request.args.get('order_dir', 'asc')

    column_map = {
        1: Vehicle.type,
        2: Vehicle.model,
        3: Vehicle.license_plate,
        4: Vehicle.driver
    }

    order_column = column_map.get(order_column_index, Vehicle.type)
    if order_dir == 'desc':
        order_column = order_column.desc()

    query = Vehicle.query.order_by(order_column).offset(start).limit(length)
    total_records = Vehicle.query.count()

    data = [{"id":vehicle.id,
             "image":base64.b64encode(vehicle.image).decode('utf-8') if vehicle.image else None,
             "type": get_vehicle_type_status_name(True).get(vehicle.type, "-"),
             "model": get_vehicle_model_status_name(True).get(vehicle.model, "-"),
             "plate": vehicle.license_plate,
             "driver": f"{vehicle.user.first_name} {vehicle.user.last_name}" if vehicle.driver else "-"}
            for vehicle in query]
    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })



@admin_page.route('/vehicle_edit/<int:id>', methods=["GET", "POST"])
@register_breadcrumbs(admin_page, ".vehicle_edit.id", "Vehicle edit")
def vehicle_edit(id):
    if id == 0:
        vehicle = Vehicle()
        form = VehicleForm()
    else:
        vehicle = Vehicle.query.get_or_404(id)
        form = VehicleForm(obj=vehicle)

    if request.method == "POST" and form.validate_on_submit():
        vehicle.type = form.type.data
        vehicle.model = form.model.data
        vehicle.year = form.year.data
        vehicle.engine_type = form.engine_type.data
        vehicle.license_plate = form.license_plate.data
        vehicle.initial_mileage = form.initial_mileage.data
        vehicle.current_mileage = form.current_mileage.data
        vehicle.registration_expiry_date = form.registration_expiry_date.data
        vehicle.driver = form.driver.data
        if form.image.data and not isinstance(form.image.data, bytes):
            file = form.image.data
            file_data  = file.read()
            vehicle.image = file_data
        vehicle.save()
        flash('Create new vehicle successfully.', 'success')
        return redirect(url_for('dashboard.vehicles'))

    img_bytes = vehicle.image  # bytes
    if not img_bytes:
        img_bytes = open(current_app.static_folder + "/images/car_img.png", 'rb').read()
    img_string = base64.b64encode(img_bytes).decode("ascii")

    return render_template("vehicle_edit.html",
                           header_title="Vehicle edit",
                           img_string=img_string,
                           form=form,
                           )

@admin_page.route('/support', methods=["GET"])
def support():
    return render_template("support.html")


@admin_page.route('/vehicle_report', methods=["GET"])
@permission_required(PermissionStatusCodes.VEHICLES)
def vehicle_report():
    report_format = request.args.get('format', '')
    if report_format:
        vehicles = Vehicle.query.all()
        if not vehicles:
            return jsonify("No data to export!"), 400

        # check format
        if report_format == 'csv':
            return export_csv(vehicles)
        elif report_format == 'xlsx':
            return export_xlsx(vehicles)
        elif report_format == 'pdf':
            return export_pdf(vehicles)
        else:
            return jsonify("Incorrect format!"), 400

    return render_template("vehicle_report.html")
