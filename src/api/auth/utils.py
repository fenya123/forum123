"""Some utilities for api package."""

import functools
from typing import Any

import jwt
from flask import abort
from flask_restx import reqparse
from jwt import InvalidTokenError

from src.config import Config
from src.users.models import User


parser = reqparse.RequestParser()
parser.add_argument("Authorization", required=True, location="headers")


def authorized_access(function_to_wrap: Any) -> Any:
    """Parse, validate and decode JWT authorization token."""
    @functools.wraps(function_to_wrap)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        parsed_arguments = parser.parse_args()
        scheme, _, token = parsed_arguments["Authorization"].partition(" ")
        if scheme != "Bearer" or token == "":  # pylint: disable=compare-to-empty-string
            return abort(401, "invalid token")

        try:
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except InvalidTokenError:
            return abort(401, "invalid token")

        if not User.get_user_by_id(decoded_token["user_id"]):
            return abort(403, "user not found")
        return function_to_wrap(*args, **kwargs)
    return wrapper
