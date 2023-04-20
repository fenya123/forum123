"""posts endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, reqparse, Resource

from src.api.auth.utils import authorized_access
from src.api.posts.utils import parse_order_by
from src.api.topics.routes import ns as topics_ns
from src.posts.models import Post
from src.topics.models import Topic


ns = Namespace("posts", path="/posts")

parser = reqparse.RequestParser()


@topics_ns.route("/<int:topic_id>/posts")
class PostsList(Resource):  # type: ignore
    """Get a list of posts of a certain topic."""

    @staticmethod
    @authorized_access(provide_user=True)
    def get(topic_id: int) -> list[dict[str, Any]] | None:
        """Get a list of posts of a certain topic."""
        parser.add_argument("order_by", type=parse_order_by, help="get a list of posts of a topic")
        sorting_parameters = parser.parse_args()
        if not Topic.get(topic_id):
            return abort(404, "topic does not exist")
        posts = Post.get_posts_list(topic_id, sorting_parameters["order_by"])
        return [{
            "id": post.id,
            "author_id": post.author_id,
            "created_at": str(post.created_at),
            "body": post.body,
            "topic_id": post.topic_id,
        } for post in posts]


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
            "author_id": post.id,
            "created_at": str(post.created_at),
            "body": post.body,
            "topic_id": post.topic_id,
        }
