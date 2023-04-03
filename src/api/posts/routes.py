"""posts endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, Resource

from src.posts.models import Post


ns = Namespace("posts", path="/posts")


@ns.route("/<int:post_id>")
class PostInfo(Resource):  # type: ignore
    """Get a post's information."""

    @staticmethod
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
