"""forum123's route module."""

from __future__ import annotations

from flask import Blueprint
from flask import render_template

from src.database import session_var
from src.users.models import User


bp = Blueprint("routes", __name__)


@bp.route("/check-unit-tests", methods=["POST"])
def check_unit_tests() -> str:
    """Route to check that application works correctly in unit-testing environment."""
    session = session_var.get()
    session.add(User(username="user from app", password_hash="password"))
    session.commit()
    return render_template("user_created.html")
