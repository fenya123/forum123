"""'api' package's routes module."""

from flask import Blueprint
from flask_restx import Api

import src.api.users.routes


bp = Blueprint("api", __name__)

api = Api(bp, prefix="/api")
api.add_namespace(src.api.users.routes.ns)
