from flask import Blueprint, render_template

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    print("Dashboard Page")
    return render_template("dashboard.html")
