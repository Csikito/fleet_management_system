from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, HiddenField,
                     BooleanField)
from wtforms.validators import DataRequired

from .util import get_permission_status_name


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
