"""forum123's route module."""

from flask import Blueprint
from flask import render_template

from src.database import session
from src.forms import RegistrationForm
from src.models import User


bp = Blueprint("routes", __name__)


@bp.route("/")
@bp.route("/index")
def index() -> str:
    """Handle index page."""
    users = session.query(User).all()
    return render_template("index.html", users=users)


@bp.route("/registration")
def registration() -> str:
    """Handle user's registration form."""
    form = RegistrationForm()
    return render_template("registration.html", form=form)
