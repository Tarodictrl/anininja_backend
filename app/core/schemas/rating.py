from typing_extensions import Type

from pydantic import BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)


class RatingBase(BaseModelConfig):
    anime_id: int | None
    kp_rating: float | None
    shikimori_rating: float | None
    anidub_rating: float | None
    myanimelist_rating: float | None
    worldart_rating: float | None
    avg_rating: float | None


class RatingUpdate(RatingBase):
    ...


class RatingCreateBase(RatingBase):
    ...


RatingCreate: Type[BaseModel] = create_response_model(RatingCreateBase, "GenreResponse")
