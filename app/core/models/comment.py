from __future__ import annotations
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.core.models.user import User


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    message: Mapped[str] = mapped_column(
        String,
    )
    comment_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
    )
    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )
    parent: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("comment.id"),
        nullable=True,
    )
    user: Mapped[User] = relationship(lazy="selectin", viewonly=True)
