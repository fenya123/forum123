"""forum123's database models module."""

from sqlalchemy import Column, Integer, String

from src.database import Base


class User(Base):  # pylint: disable=too-few-public-methods
    """A model class for User database table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # noqa: A003
    username = Column(String, nullable=False, unique=True)
