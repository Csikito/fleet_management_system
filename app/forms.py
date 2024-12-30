from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, HiddenField,
                     BooleanField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='The username field is required')])
    password = PasswordField('Password', validators=[DataRequired(message='The password field is required')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
