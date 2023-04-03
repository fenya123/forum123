"""topics endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, Resource

from src.topics.models import Topic


ns = Namespace("topics", path="/topics")


@ns.route("/<int:topic_id>")
class TopicInfo(Resource):  # type: ignore
    """Get a topic's information.."""

    @staticmethod
    def get(topic_id: int) -> dict[str, Any] | None:
        """Get a topic's information."""
        if not (topic := Topic.get(topic_id)):
            return abort(404, "Could not find a topic with id provided.")
        return {
            "author_id": topic.author_id,
            "created_at": str(topic.created_at),
            "description": topic.description,
            "title": topic.title,
        }
