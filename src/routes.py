"""forum123's route module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint
from flask import redirect, render_template, url_for

from src.database import session_var
from src.forms import PostForm, TopicForm
from src.models import Topic
from src.users.models import User
from src.users.utils import get_current_user

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
    users = User.get_users()
    current_user = get_current_user()

    return render_template("index.html", users=users, current_user=current_user)


@bp.route("/topics")
def topics() -> str | Response:
    """Handle topics page."""
    if (current_user := get_current_user()) is not None:
        topic_list = Topic.get_topics()
        return render_template("topics.html", topic_list=topic_list, current_user=current_user)
    return redirect(url_for("users.login"))


@bp.route("/topics/create", methods=["POST", "GET"])
def create_topic() -> str | Response:
    """Handle create topic page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("users.login"))
    form = TopicForm()
    if not form.validate_on_submit():
        return render_template("topics-create.html", form=form, current_user=current_user)
    Topic.create_topic(form.title.data, form.description.data, current_user.id)
    return redirect(url_for("routes.topics"))


@bp.route("/topics/<int:topic_id>")
def topic_page(topic_id: int) -> str | Response:
    """Handle topic page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("users.login"))
    if not (topic := Topic.get(topic_id)):
        return render_template("404.html", current_user=current_user)
    return render_template("topic.html", current_user=current_user, topic=topic)


@bp.route("/topics/<int:topic_id>/posts/create", methods=["POST", "GET"])
def create_post(topic_id: int) -> str | Response:  # noqa: CFQ004
    """Handle post creation page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("users.login"))
    form = PostForm()
    if not (topic := Topic.get(topic_id)):
        return render_template("404.html", current_user=current_user)
    if form.validate_on_submit():
        topic.create_post(form.body.data, current_user.id)
        return redirect(url_for("routes.topic_page", topic_id=topic.id))
    return render_template("posts-create.html", form=form, topic=topic, current_user=current_user)
