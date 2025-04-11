from flask import render_template, redirect, url_for
from flask_login import current_user


def page_no_access(error):
    if not current_user.is_authenticated:
        return redirect(url_for('login_page.login'))
    return render_template('403.html'), 403

def page_not_found(error):
    if not current_user.is_authenticated:
        return redirect(url_for('login_page.login'))
    return render_template('404.html'), 404

def page_internal_server_error(error):
    if not current_user.is_authenticated:
        return redirect(url_for('login_page.login'))
    return render_template('500.html'), 500

def get_permission_status_name(to_dict=False):
    from .models import PermissionStatusCodes
    status_name = [
        (PermissionStatusCodes.USERS ,"User"),
        (PermissionStatusCodes.PERMISSION ,"Permission"),
        (PermissionStatusCodes.VEHICLES ,"Vehicles"),
        (PermissionStatusCodes.FINANCIAL_REPORT ,"Financial report"),
        (PermissionStatusCodes.VEHICLE_REPORT ,"Vehicle report"),
        (PermissionStatusCodes.MILEAGE_REPORT ,"Mileage report"),
        (PermissionStatusCodes.TRANSPORT, "Transport"),
    ]
    if to_dict:
        return dict(status_name)
    return status_name

def get_vehicle_type_status_name(to_dict=False):
    from .models import VehicleTypeStatusCodes
    status_name = [
        (VehicleTypeStatusCodes.CAR ,"Car"),
        (VehicleTypeStatusCodes.VAN ,"Van"),
        (VehicleTypeStatusCodes.TRUCK ,"Truck"),
    ]
    if to_dict:
        return dict(status_name)
    return status_name

def get_vehicle_model_status_name(to_dict=False):
    from .models import VehicleModelStatusCodes
    status_name = [
        (VehicleModelStatusCodes.CITROEN_JUMPER ,"Citroen Jumper"),
        (VehicleModelStatusCodes.OPEL_MOVANO ,"Opel Movano"),
        (VehicleModelStatusCodes.SCANIA_R450 ,"Scania R450"),
        (VehicleModelStatusCodes.MAN_TGX ,"Man TGX"),
        (VehicleModelStatusCodes.OPEL_ASTRA ,"Opel Astra"),
        (VehicleModelStatusCodes.SEAT_IBIZA ,"Seat Ibiza"),
    ]
    if to_dict:
        return dict(status_name)
    return status_name

def get_user_id_name(to_dict=False):
    from .models import User
    users = User.query.all()
    user_list = [(user.id, f"{user.first_name} {user.last_name}") for user in users] # (id, name)
    if to_dict:
        return dict(user_list)
    return user_list

def get_transport_cargo_name(to_dict=False):
    from .models import Cargo
    status_name = [
        (Cargo.GRAIN ,"Grain"),
        (Cargo.IRON ,"Iron"),
        (Cargo.OTHER ,"Other products")
    ]
    if to_dict:
        return dict(status_name)
    return status_name