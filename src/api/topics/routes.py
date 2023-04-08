"""topics endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, reqparse, Resource

from src.api.topics.utils import parse_order_by
from src.topics.models import Topic


ns = Namespace("topics", path="/topics")

parser = reqparse.RequestParser()


@ns.route("")
class TopicList(Resource):  # type: ignore
    """Get a sorted list of all topics."""

    @staticmethod
    def get() -> list[dict[str, Any]] | None:
        """Get a sorted list of all topics."""
        parser.add_argument("order_by", type=parse_order_by, help="get a sorted list of topics")
        sorting_parameters = parser.parse_args()
        topics = Topic.get_topics(sorting_parameters["order_by"])
        return [{
            "id": topic.id,
            "author_id": topic.author_id,
            "created_at": str(topic.created_at),
            "description": topic.description,
            "title": topic.title,
        } for topic in topics]


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
