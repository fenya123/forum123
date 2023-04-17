"""'api' package's routes module."""

from flask import Blueprint
from flask_restx import Api

import src.api.auth.routes
import src.api.posts.routes
import src.api.topics.routes
import src.api.users.routes


bp = Blueprint("api", __name__)

api = Api(bp, prefix="/api")
api.add_namespace(src.api.users.routes.ns)
api.add_namespace(src.api.topics.routes.ns)
api.add_namespace(src.api.posts.routes.ns)
api.add_namespace(src.api.auth.routes.ns)
