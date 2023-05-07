"""topics endpoint module."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from flask import abort
from flask_restx import Namespace, Resource

from src.api.auth.utils import authorized_access
from src.api.topics.utils import parse_author_id, parse_datetime, parse_order_by
from src.shared import reqparse
from src.topics.models import Topic

if TYPE_CHECKING:
    from src.users.models import User

ns = Namespace("topics", path="/topics")


@ns.route("")
class TopicList(Resource):  # type: ignore
    """Work with topics."""

    @staticmethod
    @authorized_access()
    def get() -> list[dict[str, Any]] | None:
        """Get a sorted list of all topics."""
        parser = reqparse.RequestParser()
        parser.add_argument("order_by", type=parse_order_by)
        parser.add_argument("author_id", type=parse_author_id, action="append")
        parser.add_argument("created_after", type=parse_datetime)
        parser.add_argument("created_before", type=parse_datetime)
        parsed_args = parser.parse_args()
        topics = Topic.get_topics(
            sorting=parsed_args.get("order_by"),
            author_ids=parsed_args.get("author_id"),
            created_before=parsed_args.get("created_before"),
            created_after=parsed_args.get("created_after"),
        )
        return [{
            "id": topic.id,
            "author_id": topic.author_id,
            "created_at": str(topic.created_at),
            "description": topic.description,
            "title": topic.title,
        } for topic in topics]

    @staticmethod
    @authorized_access(provide_user=True)
    def post(user: User) -> dict[str, Any]:
        """Create topic and return its' info."""
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("description", required=True)
        topic_info = parser.parse_args()
        if not topic_info["title"] or not topic_info["description"]:
            abort(400, "invalid request")
        created_topic = Topic.create_topic(title=topic_info["title"],
                                           description=topic_info["description"], author_id=user.id)
        return {
            "id": created_topic.id,
            "author_id": created_topic.author_id,
            "description": created_topic.description,
            "title": created_topic.title,
        }


@ns.route("/<int:topic_id>")
class TopicInfo(Resource):  # type: ignore
    """Get a topic's information.."""

    @staticmethod
    @authorized_access()
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
