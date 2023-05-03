"""Some utilities for api.posts."""

from datetime import datetime

from flask import abort

from src.posts.models import Post


def parse_order_by(value: str) -> dict[str, str] | None:  # noqa: CFQ004  # pylint: disable=duplicate-code
    """Parse arguments provided."""
    if not value:
        return abort(400, "empty argument value is not allowed")

    try:
        parameter, order = value.split(",")
    except ValueError:
        return abort(400, "failed parsing parameters provided")

    if parameter not in Post.SORTING_FIELDS or order not in Post.SORTING_ORDER:
        return abort(400, "provided value is not allowed")
    return {"field": parameter, "order": order}


def parse_author_id(value: str) -> int | None:  # pylint: disable=duplicate-code
    """Parse author_id query parameter."""
    if not value:
        return abort(400, "empty argument value is not allowed")
    try:
        int(value)
    except ValueError:
        return abort(400, "author id must be an integer")
    return int(value)


def parse_datetime(value: str) -> datetime | None:  # pylint: disable=duplicate-code
    """Parse dates as strings and return datetime objects."""
    if not value:
        return abort(400, "empty argument value is not allowed")
    try:
        parsed_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return abort(400, "invalid datetime string")
    return parsed_datetime  # noqa: R504
