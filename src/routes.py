"""forum123's route module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint
from flask import make_response, redirect, render_template, request, url_for

from src.database import session_var
from src.forms import LoginForm, PostForm, RegistrationForm, TopicForm
from src.models import Topic, User, UserSession

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


bp = Blueprint("routes", __name__)


def get_current_user() -> User | None:
    """Use this function to get current user."""
    user_session = None
    if session_id := request.cookies.get("session_id"):
        user_session = UserSession.get_user_session_by_session_id(session_id)

    if user_session is not None:
        return user_session.user
    return None


@bp.route("/check-unit-tests", methods=["POST"])
def check_unit_tests() -> str:
    """Route to check that application works correctly in unit-testing environment."""
    session = session_var.get()
    session.add(User(username="user from app", password_hash="password"))
    session.commit()
    return render_template("user_created.html")


@bp.route("/")
@bp.route("/index")
def index() -> str:
    """Handle index page."""
    users = User.get_users()
    current_user = get_current_user()

    return render_template("index.html", users=users, current_user=current_user)


@bp.route("/registration", methods=["POST", "GET"])
def registration() -> str | Response:
    """Handle user's registration form."""
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(form.username.data, form.password.data)
        return redirect(url_for("routes.login"))
    return render_template("registration.html", form=form)


@bp.route("/login", methods=["POST", "GET"])
def login() -> str | Response:
    """Handle user's login form."""
    form = LoginForm()
    if form.validate_on_submit() and (user := User.get_user_by_credentials(form.username.data, form.password.data)):
        user_session = user.create_session()
        response = make_response(redirect(url_for("routes.topics")))
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
    return redirect(url_for("routes.login"))


@bp.route("/topics")
def topics() -> str | Response:
    """Handle topics page."""
    if (current_user := get_current_user()) is not None:
        topic_list = Topic.get_topics()
        return render_template("topics.html", topic_list=topic_list, current_user=current_user)
    return redirect(url_for("routes.login"))


@bp.route("/topics/create", methods=["POST", "GET"])
def create_topic() -> str | Response:
    """Handle create topic page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("routes.login"))
    form = TopicForm()
    if not form.validate_on_submit():
        return render_template("topics-create.html", form=form, current_user=current_user)
    Topic.create_topic(form.title.data, form.description.data, current_user.id)
    return redirect(url_for("routes.topics"))


@bp.route("/topics/<int:topic_id>")
def topic_page(topic_id: int) -> str | Response:
    """Handle topic page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("routes.login"))
    if not (topic := Topic.get(topic_id)):
        return render_template("404.html", current_user=current_user)
    return render_template("topic.html", current_user=current_user, topic=topic)


@bp.route("/topics/<int:topic_id>/posts/create", methods=["POST", "GET"])
def create_post(topic_id: int) -> str | Response:  # noqa: CFQ004
    """Handle post creation page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("routes.login"))
    form = PostForm()
    if not (topic := Topic.get(topic_id)):
        return render_template("404.html", current_user=current_user)
    if topic and form.validate_on_submit():
        topic.create_post(form.body.data, current_user.id)
        return redirect(url_for("routes.topic_page", topic_id=topic.id))
    return render_template("posts-create.html", form=form, topic=topic, current_user=current_user)
