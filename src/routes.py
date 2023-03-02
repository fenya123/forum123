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
    session = session_var.get()
    users = session.query(User).all()
    session_id = request.cookies.get("session_id")
    user_session = session.query(UserSession).filter_by(session_id=session_id).first()

    current_user = None
    if user_session is not None:
        current_user = session.query(User).filter_by(id=user_session.user_id).one()

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
    session = session_var.get()
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            user_session = user.create_session()
            response = make_response(redirect(url_for("routes.topics")))
            response.set_cookie("session_id", user_session.session_id)
            return response
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    """Log out users."""
    session = session_var.get()
    session_id = request.cookies.get("session_id")
    if session_to_delete := session.query(UserSession).filter_by(session_id=session_id).first():
        session.delete(session_to_delete)
        session.commit()
    return redirect(url_for("routes.login"))


@bp.route("/topics")
def topics() -> str | Response:
    """Handle topics page."""
    session = session_var.get()
    session_id = request.cookies.get("session_id")
    user_session = session.query(UserSession).filter_by(session_id=session_id).first()

    current_user = None
    if user_session is not None:
        current_user = session.query(User).filter_by(id=user_session.user_id).one()
        topic_list = session.query(Topic).order_by(Topic.created_at.desc()).all()
        return render_template("topics.html", topic_list=topic_list, current_user=current_user)
    return redirect(url_for("routes.login"))


@bp.route("/topics/create", methods=["POST", "GET"])
def create_topic() -> str | Response:
    """Handle create topic page."""
    session = session_var.get()
    session_id = request.cookies.get("session_id")
    user_session = session.query(UserSession).filter_by(session_id=session_id).first()

    current_user = None
    if user_session is not None:
        current_user = session.query(User).filter_by(id=user_session.user_id).one()
        form = TopicForm()
        if form.validate_on_submit():
            Topic.create_topic(form.title.data, form.description.data, current_user.id)
            return redirect(url_for("routes.topics"))
        return render_template("topics-create.html", form=form, current_user=current_user)
    return redirect(url_for("routes.login"))


@bp.route("/topics/<int:topic_id>")
def topic_page(topic_id: int) -> str | Response:
    """Handle topic page."""
    session = session_var.get()
    session_id = request.cookies.get("session_id")
    user_session = session.query(UserSession).filter_by(session_id=session_id).first()

    current_user = None
    if user_session is not None:
        current_user = session.query(User).filter_by(id=user_session.user_id).one()
        if not (topic := session.query(Topic).filter_by(id=topic_id).first()):
            return render_template("404.html", current_user=current_user)
        return render_template("topic.html", current_user=current_user, topic=topic)
    return redirect(url_for("routes.login"))


@bp.route("/topics/<int:topic_id>/posts/create", methods=["POST", "GET"])
def create_post(topic_id: int) -> str | Response:  # noqa: CFQ004
    """Handle post creation page."""
    session = session_var.get()
    session_id = request.cookies.get("session_id")
    user_session = session.query(UserSession).filter_by(session_id=session_id).first()

    current_user = None
    if user_session is not None:
        current_user = session.query(User).filter_by(id=user_session.user_id).one()
        form = PostForm()
        if not (topic := session.query(Topic).filter_by(id=topic_id).first()):
            return render_template("404.html", current_user=current_user)
        if topic and form.validate_on_submit():
            topic.create_post(form.body.data, current_user.id)
            return redirect(url_for("routes.topic_page", topic_id=topic.id))
        return render_template("posts-create.html", form=form, topic=topic, current_user=current_user)
    return redirect(url_for("routes.login"))
