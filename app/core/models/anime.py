from __future__ import annotations

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.db import Base
from app.core.models.genre import Genre
from app.core.models.director import Director
from app.core.models.studio import Studio
from app.core.models.poster import Poster
from app.core.models.rating import Rating


class AnimeGenre(Base):
    __tablename__ = "anime_genre"

    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
        primary_key=True,
    )
    genre_id: Mapped[str] = mapped_column(
        Integer,
        ForeignKey("genre.id"),
        primary_key=True,
    )


class AnimeDirector(Base):
    __tablename__ = "anime_director"

    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
        primary_key=True,
    )
    director_id: Mapped[str] = mapped_column(
        Integer,
        ForeignKey("director.id"),
        primary_key=True,
    )


class Anime(Base):
    __tablename__ = "anime"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    alternative_names: Mapped[list[str]] = mapped_column(
        ARRAY(String(200)),
    )
    status: Mapped[str] = mapped_column(
        String(200),
    )
    count_series: Mapped[int] = mapped_column(
        Integer,
    )
    description: Mapped[str] = mapped_column(
        String(200),
    )
    studio_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("studio.id")
    )
    year: Mapped[int] = mapped_column(
        Integer,
    )
    season: Mapped[int] = mapped_column(
        Integer,
    )
    type: Mapped[str] = mapped_column(
        String,
    )
    age: Mapped[str] = mapped_column(
        String,
    )
    kodik_link: Mapped[str] = mapped_column(
        String,
    )

    genres: Mapped[list[Genre]] = relationship(secondary="anime_genre", lazy="selectin", viewonly=True)
    directors: Mapped[list[Director]] = relationship(secondary="anime_director", lazy="selectin", viewonly=True)
    studio: Mapped[Studio] = relationship(lazy="selectin", viewonly=True)
    poster: Mapped[Poster] = relationship(lazy="selectin", viewonly=True)
    rating: Mapped[Rating] = relationship(lazy="selectin", viewonly=True)
