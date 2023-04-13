"""Some utilities for api.posts."""

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
