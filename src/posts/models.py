"""Models module of 'posts' package."""

from __future__ import annotations

from typing import Final, TYPE_CHECKING

from sqlalchemy import Column, DateTime, desc, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base, session_var

if TYPE_CHECKING:
    from datetime import datetime
    from src.users.models import User


class Post(Base):
    """A model class for posts table."""

    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    author_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    body: str = Column(String(123), nullable=False)
    topic_id: int = Column(Integer, ForeignKey("topics.id"), nullable=False)
    author: User = relationship("User", uselist=False)

    SORTING_FIELDS: Final = ("created_at")
    SORTING_ORDER: Final = ("asc", "desc")

    @staticmethod
    def get_post_by_id(post_id: int) -> Post | None:
        """Use this method to get a post with a certain id."""
        session = session_var.get()
        return session.query(Post).filter_by(id=post_id).first()

    @staticmethod
    def get_posts_list(topic_id: int, sorting: dict[str, str] | None = None) -> list[Post]:
        """Use this method to get a list of posts of a certain topic."""
        sorting = {"field": "created_at", "order": "asc"} if sorting is None else sorting
        session = session_var.get()
        if sorting["order"] == "desc":
            return session.query(Post).filter_by(topic_id=topic_id).order_by(desc(sorting["field"])).all()
        return session.query(Post).filter_by(topic_id=topic_id).order_by(sorting["field"]).all()
