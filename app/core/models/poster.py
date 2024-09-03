from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Poster(Base):
    __tablename__ = "poster"

    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
        primary_key=True,
    )
    fullsize: Mapped[str] = mapped_column(
        String,
    )
    big: Mapped[str] = mapped_column(
        String,
    )
    small: Mapped[str] = mapped_column(
        String,
    )
    medium: Mapped[str] = mapped_column(
        String,
    )
    huge: Mapped[str] = mapped_column(
        String,
    )
