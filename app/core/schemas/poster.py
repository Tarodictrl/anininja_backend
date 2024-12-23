from typing_extensions import Type

from pydantic import BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)


class PosterBase(BaseModelConfig):
    anime_id: int | None
    fullsize: str | None
    big: str | None
    small: str | None
    medium: str | None
    huge: str | None


class PosterUpdate(PosterBase):
    ...


class PosterCreateBase(PosterBase):
    ...


PosterResponse: Type[BaseModel] = create_response_model(PosterCreateBase, "PosterResponse")
