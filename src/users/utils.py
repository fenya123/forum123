"""Some utilities for working with users."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import request

from src.users.models import UserSession

if TYPE_CHECKING:
    from src.users.models import User


def get_current_user() -> User | None:  # pragma: no cover
    """Use this function to get current user."""
    user_session = None
    if session_id := request.cookies.get("session_id"):
        user_session = UserSession.get_user_session_by_session_id(session_id)

    if user_session is not None:
        return user_session.user
    return None
