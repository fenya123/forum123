"""forum123's database models module."""

from __future__ import annotations

import hashlib
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base, session_var


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


class UserSession(Base):  # pylint: disable=too-few-public-methods
    """A model class for user_session table."""

    __tablename__ = "user_session"

    id = Column(Integer, primary_key=True)  # noqa: A003
    session_id = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Topic(Base):
    """A model class for topics table."""

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)  # noqa: A003
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    description = Column(String(123), nullable=False)
    title = Column(String(30), nullable=False)
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


class Post(Base):  # pylint: disable=too-few-public-methods
    """A model class for posts table."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)  # noqa: A003
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    body = Column(String(123), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    author: User = relationship("User", uselist=False)
