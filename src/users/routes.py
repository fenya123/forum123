"""Routes module of 'users' package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint
from flask import make_response, redirect, render_template, request, url_for

from src.users.forms import LoginForm, RegistrationForm
from src.users.models import User, UserSession

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


bp = Blueprint("users", __name__, template_folder="templates")


def get_current_user() -> User | None:
    """Use this function to get current user."""
    user_session = None
    if session_id := request.cookies.get("session_id"):
        user_session = UserSession.get_user_session_by_session_id(session_id)

    if user_session is not None:
        return user_session.user
    return None


@bp.route("/registration", methods=["POST", "GET"])
def registration() -> str | Response:
    """Handle user's registration form."""
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(form.username.data, form.password.data)
        return redirect(url_for("users.login"))
    return render_template("registration.html", form=form)


@bp.route("/login", methods=["POST", "GET"])
def login() -> str | Response:
    """Handle user's login form."""
    form = LoginForm()
    if form.validate_on_submit() and (user := User.get_user_by_credentials(form.username.data, form.password.data)):
        user_session = user.create_session()
        response = make_response(redirect(url_for("topics.topics")))
        response.set_cookie("session_id", user_session.session_id)
        return response
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    """Log out users."""
    session_id = request.cookies.get("session_id")
    session_to_delete = None
    if session_id is not None:
        session_to_delete = UserSession.get_user_session_by_session_id(session_id)
    if session_to_delete:
        session_to_delete.delete()
    return redirect(url_for("users.login"))
