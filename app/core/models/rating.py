from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Rating(Base):
    __tablename__ = "rating"

    anime_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("anime.id"),
        primary_key=True,
    )
    kp_rating: Mapped[float] = mapped_column(
        Float,
    )
    shikimori_rating: Mapped[float] = mapped_column(
        Float,
    )
    anidub_rating: Mapped[float] = mapped_column(
        Float,
    )
    myanimelist_rating: Mapped[float] = mapped_column(
        Float,
    )
    worldart_rating: Mapped[float] = mapped_column(
        Float,
    )
