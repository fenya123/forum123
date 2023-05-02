"""forum123's configuration module."""

import os


class Config():  # pylint: disable=too-few-public-methods
    """Configuration class."""

    POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")

    PROXIES_X_FOR = int(os.environ.get("PROXIES_X_FOR", 0))
    PROXIES_X_HOST = int(os.environ.get("PROXIES_X_HOST", 0))
    PROXIES_X_PREFIX = int(os.environ.get("PROXIES_X_PREFIX", 0))
    PROXIES_X_PROTO = int(os.environ.get("PROXIES_X_PROTO", 0))

    RESTX_ERROR_404_HELP = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "bob")

    # next will be listed options derived from the options above
    # we need some of them to use as an aliases for convenience

    DATABASE_CONNECTION_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    PROXIES = any((PROXIES_X_FOR, PROXIES_X_HOST, PROXIES_X_PREFIX, PROXIES_X_PROTO))
