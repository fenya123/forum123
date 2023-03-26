"""Routes module of 'index' package."""

from __future__ import annotations

from flask import Blueprint
from flask import render_template

from src.users.models import User
from src.users.utils import get_current_user


bp = Blueprint("index", __name__, template_folder="templates")


@bp.route("/")
@bp.route("/index")
def index() -> str:
    """Handle index page."""
    users = User.get_users()
    current_user = get_current_user()

    return render_template("index.html", users=users, current_user=current_user)
