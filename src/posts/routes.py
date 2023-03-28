"""Routes module of 'posts' package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint
from flask import redirect, render_template, url_for

from src.posts.forms import PostForm
from src.topics.models import Topic
from src.users.utils import get_current_user

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


bp = Blueprint("posts", __name__, template_folder="templates")


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
        return redirect(url_for("topics.topic_page", topic_id=topic.id))
    return render_template("posts-create.html", form=form, topic=topic, current_user=current_user)
