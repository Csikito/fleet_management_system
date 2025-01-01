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

