"""Main package for source code."""

from flask import Flask

from src.routes import bp as routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp)
