"""forum123's route module."""

from flask import Blueprint
from flask import render_template

from src.forms import RegistrationForm


bp = Blueprint("routes", __name__)


@bp.route("/")
@bp.route("/index")
def index() -> str:
    """Use this view function to check whether Flask is installed properly."""
    return "Hello, wordl!"


@bp.route("/registration")
def registration() -> str:
    """Handle user's registration form."""
    form = RegistrationForm()
    return render_template("registration.html", form=form)
