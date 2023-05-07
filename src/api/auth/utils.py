"""Some utilities for api package."""

from __future__ import annotations

import functools
from typing import Any, ParamSpec, TYPE_CHECKING, TypeVar

import jwt
from flask import abort
from jwt import InvalidTokenError

from src.config import Config
from src.shared import reqparse
from src.users.models import User

if TYPE_CHECKING:
    from collections.abc import Callable


T = TypeVar("T")
P = ParamSpec("P")


def parse_token_data(header: str) -> dict[str, int]:
    """Parse and validate JWT authorization token from Authorization request header."""
    scheme, _, token = header.partition(" ")
    if scheme != "Bearer" or token == "":  # pylint: disable=compare-to-empty-string
        return abort(401, "invalid token")
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except InvalidTokenError:
        return abort(401, "invalid token")


def authorized_access(provide_user: bool = False) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Check whether user has access or not."""
    def decorator(function_to_wrap: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(function_to_wrap)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            parser = reqparse.RequestParser()
            parser.add_argument("Authorization", required=True, type=parse_token_data, location="headers")
            decoded_token = parser.parse_args()["Authorization"]
            if not (user := User.get_user_by_id(decoded_token["user_id"])):
                return abort(403, "user not found")
            if provide_user:
                kwargs["user"] = user
            return function_to_wrap(*args, **kwargs)
        return wrapper
    return decorator
