"""Main package for source code."""

from flask import Flask

from src import routes
from src.config import Config

app = Flask(__name__)
app.register_blueprint(routes.bp)
app.config.from_object(Config)
