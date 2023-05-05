"""This module provides a customized version of flask-restx's reqparse features."""

from typing import Any, NoReturn

from flask import abort
from flask_restx import reqparse


class RequestParser(reqparse.RequestParser):  # type: ignore
    """Customized version of flask-restx's RequestParser class."""

    def __init__(self, *args: list[Any], **kwargs: Any) -> None:  # pragma: no cover
        """Init method."""
        if "argument_class" not in kwargs:
            kwargs["argument_class"] = Argument
        super().__init__(*args, **kwargs)


class Argument(reqparse.Argument):  # type: ignore
    """Customized version of flask-restx's Argument class."""

    def handle_validation_error(self, error: str | Exception, bundle_errors: bool) -> NoReturn:  # pragma: no cover
        """Reraise exception from parser function."""
        if isinstance(error, str):  # exceptions raised by flask-restx request parser itself
            abort(400, error)
        raise error  # any other error caught by flask-restx request parser
