"""Models module of 'users' package."""

from __future__ import annotations

import hashlib
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base, session_var


class User(Base):
    """A model class for User database table."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    username: str = Column(String, nullable=False, unique=True)
    password_hash: str = Column(String(64), nullable=False)

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password: str) -> None:
        """Use this method to set hashed password to User."""
        self.password_hash = self._get_password_hash(password)

    def check_password(self, password_to_check: str) -> bool:
        """Use this method to check User's password."""
        return self._get_password_hash(password_to_check) == self.password_hash

    @classmethod
    def create_user(cls, username: str, password: str) -> User:
        """Use this method to create a new user."""
        new_user = cls(username=username, password_hash=User._get_password_hash(password=password))
        session = session_var.get()
        session.add(new_user)
        session.commit()
        return new_user

    def create_session(self) -> UserSession:
        """Use this method to create a new session."""
        new_session = UserSession(session_id=str(uuid.uuid4()), user_id=self.id)
        session = session_var.get()
        session.add(new_session)
        session.commit()
        return new_session

    @staticmethod
    def get_users() -> list[User]:
        """Use this method to get all users from users table."""
        session = session_var.get()
        return session.query(User).all()

    @staticmethod
    def get_user_by_credentials(username: str, password: str) -> User | None:
        """Use this method to fetch a user from users table with a specific username and password."""
        session = session_var.get()
        user_to_fetch: User | None = session.query(User).filter_by(username=username).first()
        if user_to_fetch and user_to_fetch.check_password(password):
            return user_to_fetch
        return None

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        """Use this method to fetch a user from users table with a specific id."""
        session = session_var.get()
        user_to_fetch: User | None = session.query(User).filter_by(id=user_id).first()
        return user_to_fetch


class UserSession(Base):
    """A model class for user_session table."""

    __tablename__ = "user_session"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    session_id: str = Column(String, nullable=False, unique=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    user: User = relationship("User", uselist=False)

    def delete(self) -> None:
        """Use this method to delete a user session."""
        session = session_var.get()
        session.delete(self)
        session.commit()

    @staticmethod
    def get_user_session_by_session_id(session_id: str) -> UserSession | None:
        """Use this method to get a user session with a certain id."""
        session = session_var.get()
        return session.query(UserSession).filter_by(session_id=session_id).first()
