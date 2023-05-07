"""auth endpoint module."""

import jwt
from flask import abort
from flask_restx import Namespace, Resource

from src.config import Config
from src.shared import reqparse
from src.users.models import User


ns = Namespace("auth", path="/auth")


@ns.route("")
class AuthEndpoint(Resource):  # type: ignore
    """API authentication class."""

    @staticmethod
    def post() -> str | None:
        """Authenticate credentials and return JWT token."""
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        credentials = parser.parse_args()
        if not (user := User.get_user_by_credentials(credentials["username"], credentials["password"])):
            return abort(400, "couldn't find user with credentials provided")
        return jwt.encode({"user_id": user.id}, Config.SECRET_KEY, algorithm="HS256")
