"""forum123's configuration module."""

import os


class Config():  # pylint: disable=too-few-public-methods
    """Configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "bob")
