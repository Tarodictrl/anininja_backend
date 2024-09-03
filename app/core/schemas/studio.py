from typing_extensions import Type

from pydantic import BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)


class StudioBase(BaseModelConfig):
    name: str


class StudioUpdate(StudioBase):
    ...


class StudioCreate(StudioBase):
    ...


class StudioResponseBase(StudioBase):
    id: int


StudioResponse: Type[BaseModel] = create_response_model(StudioResponseBase, "GenreResponse")
