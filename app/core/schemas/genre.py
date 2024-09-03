from typing_extensions import Type

from pydantic import BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)


class GenreBase(BaseModelConfig):
    name: str


class GenreUpdate(GenreBase):
    ...


class GenreCreate(GenreBase):
    ...


class GenreResponseBase(GenreBase):
    id: int


GenreResponse: Type[BaseModel] = create_response_model(GenreResponseBase, "GenreResponse")
