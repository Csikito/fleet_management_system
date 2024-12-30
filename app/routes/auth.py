from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user
from app.forms import LoginForm
from app.models import User


login_page = Blueprint('login_page', __name__)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            remember  = login_form.remember.data

            user = User.query.filter_by(username=username).first()
            if user and user.password and user.check_password(password=password):
                if user.active:
                    login_user(user, remember=remember)
                    return redirect(url_for('dashboard.dashboard'))
                else:
                    flash('Your account is inactive. Please contact support.', 'Info')
            else:
                flash('Invalid username or password.', 'Info')

    return render_template('login.html', form=login_form)




@login_page.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page.login'))
