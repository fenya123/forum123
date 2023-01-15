"""forum123's database models module."""

import hashlib

from sqlalchemy import Column, Integer, String

from src.database import Base


class User(Base):
    """A model class for User database table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # noqa: A003
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)

    def _get_password_hash(self, password: str) -> str:  # pylint: disable=no-self-use
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password: str) -> None:
        """Use this method to set hashed password to User."""
        self.password_hash = self._get_password_hash(password)

    def check_password(self, password_to_check: str) -> bool:
        """Use this method to check User's password."""
        return self._get_password_hash(password_to_check) == self.password_hash
