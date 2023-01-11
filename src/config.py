"""forum123's configuration module."""

import os


class Config():  # pylint: disable=too-few-public-methods
    """Configuration class."""

    DATABASE_CONNECTION_URL = os.environ.get("DATABASE_CONNECTION_URL",
                                             "postgresql://postgres:@localhost:5432/postgres")
    SECRET_KEY = os.environ.get("SECRET_KEY", "bob")
