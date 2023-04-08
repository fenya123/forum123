"""Some utilities for api.topics."""


from flask import abort

from src.topics.models import Topic


def parse_order_by(value: str) -> dict[str, str] | None:  # noqa: CFQ004  # pylint: disable=duplicate-code
    """Parse arguments provided."""
    if not value:
        return abort(400, "empty argument value is not allowed")

    try:
        parameter, order = value.split(",")
    except ValueError:
        return abort(400, "failed parsing parameters provided")

    if parameter not in Topic.SORTING_FIELDS or order not in Topic.SORTING_ORDER:
        return abort(400, "provided value is not allowed")
    return {"field": parameter, "order": order}
