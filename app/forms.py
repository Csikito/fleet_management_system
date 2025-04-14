import re
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, HiddenField,
                     BooleanField, FloatField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from .util import (get_permission_status_name, get_vehicle_type_status_name, get_vehicle_model_status_name,
                   get_user_id_name, get_transport_cargo_name)
from .models import Permission


def validate_phone(form, field):
    phone_number = field.data
    if not re.match(r'^\+?\d{10,15}$', phone_number):
        raise ValidationError('Invalid phone number. It must be 10-15 digits and can start with a "+".')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='The username field is required')])
    password = PasswordField('Password', validators=[DataRequired(message='The password field is required')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class PermissionForm(FlaskForm):
    name = StringField('Permission name', validators=[DataRequired(message='The permission name field is required'),
                       Length(min=3, max=200, message='Username must be in 3 to 200 characters')])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boolean_fields = []
        permissions = get_permission_status_name(to_dict=True)
        formdata = kwargs.get('formdata', None)

        for perm_id, perm_name in permissions.items():
            field_data = False
            if formdata:  # if POST data
                field_name = str(perm_id)
                field_data = formdata.get(field_name) == 'y'  # We look at the value from the POST data

            unbound_field = BooleanField(perm_name)
            bound_field = unbound_field.bind(form=self, name=str(perm_id))
            bound_field.data = field_data
            self._fields[perm_id] = bound_field
            self.boolean_fields.append((perm_id, bound_field))


class MatchingPasswordsForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message='The password name field is required'),
                       Length(min=5, max=200, message='password must be in 5 to 200 characters')])
    repeat_password = PasswordField('Repeat Password',
                                     validators=[EqualTo('password', message='Passwords must match')])

class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message='The first name field is required')])
    last_name = StringField('Last name', validators=[DataRequired(message='The last name field is required')])
    email = StringField('Email', validators=[DataRequired(message='The Email field is required'),
                                                    Email(message='Not a valid email address')])
    phone = StringField('Phone', validators=[DataRequired(message='The phone field is required'), validate_phone])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    username = StringField('Username', validators=[DataRequired(message='The Username field is required')])
    active = BooleanField("Active", default=True)
    permission = SelectField("Permission")

    submit = SubmitField('Save')

    def __init__(self,*args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.permission.choices = [(perm.id, perm.name) for perm in Permission.query.all()]


class NewUserForm(UserForm, MatchingPasswordsForm):
    pass



class EditUserForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username.render_kw = {'readonly': True}


class VehicleForm(FlaskForm):
    type = SelectField("Type", choices=get_vehicle_type_status_name())
    model = SelectField("Manufacturer/Model", choices=get_vehicle_model_status_name())
    year = IntegerField('Year', validators=[DataRequired(message='The year field is required')])
    engine_type = SelectField("Engine type", choices=[(1,"Petrol"), (2,"Diesel")])
    license_plate = StringField('License plate', validators=[DataRequired(message='The License plate field is required')])
    image = FileField('Vehicle image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    initial_mileage = IntegerField('Initial mileage', validators=[DataRequired(message='The initial mileage name field is required')])
    current_mileage = IntegerField('Current mileage')
    registration_expiry_date = DateField('Registration expiry date',
                                                  format='%Y-%m-%d',
                                                  validators=[DataRequired(message='The registration expiry date field is required')])
    driver = SelectField("Driver", coerce=int, choices=get_user_id_name())

    submit = SubmitField('Save')


class TransportForm(FlaskForm):
    delivered_by = SelectField("Delivered by", coerce=int, choices=get_user_id_name())
    origin = StringField('Origin', validators=[DataRequired(message='The origin field is required')])
    destination = StringField('Destination', validators=[DataRequired(message='The destination field is required')])
    distance = IntegerField('Distance (km)')
    cargo = SelectField("Cargo", choices=get_transport_cargo_name())
    amount = FloatField('Weight of the shipment (kg)', validators=[DataRequired(message='The weight of the shipment field is required')])
    unit_price = FloatField('Unit price', validators=[DataRequired(message='The unit price field is required')])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(message='The date field is required')])

    submit = SubmitField('Save')
