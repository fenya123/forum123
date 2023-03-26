"""Main package for source code."""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import src.users.routes
from src import routes
from src.config import Config

app = Flask(__name__)
app.register_blueprint(routes.bp)
app.register_blueprint(src.users.routes.bp)
app.config.from_object(Config)


if Config.PROXIES:  # pragma: no cover
    # flask app has to know that it's behind a proxy
    # see: https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
    app.wsgi_app = ProxyFix(  # type: ignore
        app.wsgi_app,
        x_for=Config.PROXIES_X_FOR,
        x_proto=Config.PROXIES_X_PROTO,
        x_host=Config.PROXIES_X_HOST,
        x_prefix=Config.PROXIES_X_PREFIX,
    )
