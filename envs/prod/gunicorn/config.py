accesslog = "-"  # here "-" means stdout

# gunicorn listens all connections but it's still secure
# since it's run in isolated docker network and only rev-proxy has access to it
bind = "0.0.0.0:5000"

errorlog = "-"  # here "-" means stdout

wsgi_app = "src.app:app"
