"""Database utils."""

from sqlalchemy import text

from src.database import Base, engine


def set_autoincrement_counters():
    """Set initial value for all autoincremented sequences in db tables.

    This is needed to avoid conflicts between rows created by fixtures
    and values created by the app itself.

    For example:
        fixture creates a new user with id = 1
        test calls application endpoint which will create another user
        since id column in fixtures was provided by hands, then
        autoincrement key is not switched to the next value and user created by
        application will have id = 1 as well. This will cause and error
        because application is trying to add a user with primary key which already exists.

    So this function just sets autoincrement counter for `id` columns in all database tables.
    """
    queries = ""
    for tablename in Base.metadata.tables.keys():
        queries += f"ALTER SEQUENCE {tablename}_id_seq RESTART WITH 10000;"
    with engine.connect() as connection:
        connection.execute(text(queries))
