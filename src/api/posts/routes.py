"""posts endpoint module."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from flask import abort
from flask_restx import Namespace, Resource

from src.api.auth.utils import authorized_access
from src.api.posts.utils import parse_author_id, parse_datetime, parse_order_by
from src.api.topics.routes import ns as topics_ns
from src.posts.models import Post
from src.shared import reqparse
from src.topics.models import Topic

if TYPE_CHECKING:
    from src.users.models import User


ns = Namespace("posts", path="/posts")


@topics_ns.route("/<int:topic_id>/posts")
class PostsList(Resource):  # type: ignore
    """Work with posts."""

    @staticmethod
    @authorized_access()
    def get(topic_id: int) -> list[dict[str, Any]] | None:
        """Get a list of posts of a certain topic."""
        parser = reqparse.RequestParser()
        parser.add_argument("order_by", type=parse_order_by)  # pylint: disable=duplicate-code
        parser.add_argument("author_id", type=parse_author_id, action="append")
        parser.add_argument("created_after", type=parse_datetime)
        parser.add_argument("created_before", type=parse_datetime)
        parsed_args = parser.parse_args()
        if not Topic.get(topic_id):
            return abort(404, "topic does not exist")
        posts = Post.get_posts_list(
            topic_id,
            sorting=parsed_args.get("order_by"),  # pylint: disable=duplicate-code
            author_ids=parsed_args.get("author_id"),
            created_before=parsed_args.get("created_before"),
            created_after=parsed_args.get("created_after"),
        )
        return [{
            "id": post.id,
            "author_id": post.author_id,
            "created_at": str(post.created_at),
            "body": post.body,
            "topic_id": post.topic_id,
        } for post in posts]

    @staticmethod
    @authorized_access(provide_user=True)
    def post(topic_id: int, user: User) -> dict[str, Any]:
        """Create a new post."""
        parser = reqparse.RequestParser()
        parser.add_argument("body", required=True)
        post_info = parser.parse_args()
        if not (topic := Topic.get(topic_id)):
            return abort(404, "topic does not exist")
        created_post = topic.create_post(body=post_info["body"], author_id=user.id)
        return {
            "id": created_post.id,
            "author_id": created_post.author_id,
            "body": created_post.body,
            "created_at": str(created_post.created_at),
            "topic_id": created_post.topic_id,
        }


@ns.route("/<int:post_id>")
class PostInfo(Resource):  # type: ignore
    """Get a post's information."""

    @staticmethod
    @authorized_access()
    def get(post_id: int) -> dict[str, Any] | None:
        """Get a post's information."""
        if not (post := Post.get_post_by_id(post_id)):
            return abort(404, "Could not find a post with id provided.")
        return {
            "id": post.id,
            "author_id": post.author_id,
            "created_at": str(post.created_at),
            "body": post.body,
            "topic_id": post.topic_id,
        }
