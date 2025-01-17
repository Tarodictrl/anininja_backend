from __future__ import annotations

from datetime import date

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.core.models.anime import Anime


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    login: Mapped[str] = mapped_column(
        String,
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    avatar: Mapped[str] = mapped_column(
        String,
        default="https://img.anininja.ru/avatar/placeholder.jpeg"
    )
    role: Mapped[str] = mapped_column(
        String,
        default="user"
    )
    vk_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    registration_date: Mapped[date] = mapped_column(
        Date,
        default=date.today()
    )
    user_list: Mapped[list[UserList]] = relationship(lazy="selectin")


class UserList(Base):
    __tablename__ = "user_list"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        primary_key=True,
    )
    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
        primary_key=True,
    )
    status: Mapped[str] = mapped_column(
        String,
    )

    anime: Mapped[Anime] = relationship(lazy="selectin")
