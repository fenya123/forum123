"""Routes module of 'topics' package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint
from flask import redirect, render_template, url_for

from src.topics.forms import TopicForm
from src.topics.models import Topic
from src.users.utils import get_current_user

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


bp = Blueprint("topics", __name__, template_folder="templates")


@bp.route("/topics/<int:topic_id>")
def topic_page(topic_id: int) -> str | Response:
    """Handle topic page."""
    if (current_user := get_current_user()) is None:
        return redirect(url_for("users.login"))
    if not (topic := Topic.get(topic_id)):
        return render_template("404.html", current_user=current_user)
    return render_template("topic.html", current_user=current_user, topic=topic)


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
    return redirect(url_for("topics.topics"))
