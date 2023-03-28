"""Models module of 'topics' package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base, session_var
from src.posts.models import Post

if TYPE_CHECKING:
    from datetime import datetime
    from src.users.models import User


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
