"""Periferals required for SQLAlchemy to function."""

import contextvars

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from src.config import Config


config = Config()

# will allow us to connect to PostgreSQL database
engine = create_engine(config.DATABASE_CONNECTION_URL)

# will allow us to send SQL queries to database associated with engine
_session = scoped_session(sessionmaker(bind=engine))

# will allow us to map relation tables from PostgreSQL to python classes
# each model must inherit this Base class
Base = declarative_base()


# will allow us to easily patch db session for test environment
# via session_var.set() and session_var.get()
session_var = contextvars.ContextVar("session", default=_session)
