"""users endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, Resource

from src.users.models import User


ns = Namespace("users", path="/users")


@ns.route("/<int:user_id>")
class UserInfo(Resource):  # type: ignore
    """Get user's id and name."""

    @staticmethod
    def get(user_id: int) -> dict[str, Any] | None:
        """Get user's id and name."""
        if not (user := User.get_user_by_id(user_id)):
            return abort(404, "Could not find a user with id provided.")
        return {
            "id": user.id,
            "name": user.username,
        }
