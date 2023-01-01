"""forum123's route module."""

from flask import Blueprint


bp = Blueprint("routes", __name__)


@bp.route("/")
@bp.route("/index")
def index() -> str:  # pylint: disable=unused-variable
    """Use this view function to check whether Flask is installed properly."""
    return "Hello, wordl!"
