from typing_extensions import Type

from pydantic import Field, BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.poster import PosterBase
from app.core.schemas.studio import StudioBase
from app.core.schemas.rating import RatingBase
from app.core.schemas.director import DirectorBase
from app.core.schemas.genre import GenreBase
from app.core.schemas.base import (
    create_response_model,
)


class AnimeBase(BaseModelConfig):
    name: str
    alternative_names: list[str] | None = Field(default_factory=list, alias="alternativeNames")
    status: str | None = Field(default=None)
    count_series: int = Field(default=0, alias="countSeries")
    description: str | None = Field(default=None)
    year: int | None = Field(default=None)
    season: int | None = Field(default=None)
    type: str | None = Field(default=None)
    age: str | None = Field(default=None)
    kodik_link: str | None = Field(default=None)
    url: str | None = Field(default=None)


class AnimeUpdate(AnimeBase):
    ...


class AnimeCreate(AnimeBase):
    ...


class AnimeResponseBase(AnimeBase):
    id: int
    poster: PosterBase | None
    rating: RatingBase | None
    directors: list[DirectorBase] | None = Field(default_factory=list)
    genres: list[GenreBase] | None = Field(default_factory=list)
    studios: list[StudioBase] | None = Field(default_factory=list)


AnimeResponse: Type[BaseModel] = create_response_model(AnimeResponseBase, "AnimeResponse")
