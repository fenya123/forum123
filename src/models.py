"""forum123's database models module."""

from __future__ import annotations

import hashlib
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base, session_var

if TYPE_CHECKING:
    from datetime import datetime


class User(Base):
    """A model class for User database table."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    username: str = Column(String, nullable=False, unique=True)
    password_hash: str = Column(String(64), nullable=False)

    def _get_password_hash(self, password: str) -> str:  # pylint: disable=no-self-use
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password: str) -> None:
        """Use this method to set hashed password to User."""
        self.password_hash = self._get_password_hash(password)

    def check_password(self, password_to_check: str) -> bool:
        """Use this method to check User's password."""
        return self._get_password_hash(password_to_check) == self.password_hash

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        """Use this method to create a new user."""
        new_user = cls(username=username, password_hash=hashlib.sha256(password.encode()).hexdigest())
        session = session_var.get()
        session.add(new_user)
        session.commit()

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


class Topic(Base):
    """A model class for topics table."""

    __tablename__ = "topics"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    author_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    description: str = Column(String(123), nullable=False)
    title: str = Column(String(30), nullable=False)
    author: User = relationship("User", uselist=False)
    posts: list[Post] = relationship("Post", order_by="Post.created_at")

    @classmethod
    def create_topic(cls, title: str, description: str, author_id: int) -> None:
        """Use this method to create a new topic."""
        new_topic = cls(title=title, description=description, author_id=author_id)
        session = session_var.get()
        session.add(new_topic)
        session.commit()

    def create_post(self, body: str, author_id: int) -> None:
        """Use this method to create a new post."""
        new_post = Post(body=body, author_id=author_id, topic_id=self.id)
        session = session_var.get()
        session.add(new_post)
        session.commit()

    @staticmethod
    def get_topics() -> list[Topic]:
        """Use this method to get all topics from topics table."""
        session = session_var.get()
        return session.query(Topic).order_by(Topic.created_at.desc()).all()

    @staticmethod
    def get(topic_id: int) -> Topic | None:
        """Use this method to get a topic with a certain id."""
        session = session_var.get()
        return session.query(Topic).filter_by(id=topic_id).first()


class Post(Base):  # pylint: disable=too-few-public-methods
    """A model class for posts table."""

    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    author_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    body: str = Column(String(123), nullable=False)
    topic_id: int = Column(Integer, ForeignKey("topics.id"), nullable=False)
    author: User = relationship("User", uselist=False)
