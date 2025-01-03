from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, HiddenField,
                     BooleanField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

from .util import get_permission_status_name
from .models import Permission


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='The username field is required')])
    password = PasswordField('Password', validators=[DataRequired(message='The password field is required')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class PermissionForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(message='The username field is required')])
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
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat password')


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message='The first name field is required')])
    last_name = StringField('Last name', validators=[DataRequired(message='The last name field is required')])
    email = StringField('Email', validators=[DataRequired(message='The email field is required')])
    phone = StringField('Phone', validators=[DataRequired(message='The phone field is required')])
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
