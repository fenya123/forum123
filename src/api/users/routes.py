"""users endpoint module."""

from typing import Any

from flask import abort
from flask_restx import Namespace, Resource

from src.api.auth.utils import authorized_access
from src.api.users.utils import parse_order_by
from src.shared import reqparse
from src.users.models import User


ns = Namespace("users", path="/users")


@ns.route("")
class UserList(Resource):  # type: ignore
    """Get a list of all users, sorted if needed."""

    @staticmethod
    @authorized_access()
    def get() -> list[dict[str, Any]] | None:
        """Get a list of all users, sorted if needed."""
        parser = reqparse.RequestParser()
        parser.add_argument("order_by", type=parse_order_by, help="get a sorted list of users")
        sorting_parameters = parser.parse_args()
        users = User.get_users(sorting_parameters["order_by"])
        return [{"id": user.id, "username": user.username} for user in users]


@ns.route("/<int:user_id>")
class UserInfo(Resource):  # type: ignore
    """Get user's id and name."""

    @staticmethod
    @authorized_access()
    def get(user_id: int) -> dict[str, Any] | None:
        """Get user's id and name."""
        if not (user := User.get_user_by_id(user_id)):
            return abort(404, "Could not find a user with id provided.")
        return {
            "id": user.id,
            "name": user.username,
        }
