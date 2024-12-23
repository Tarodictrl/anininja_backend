from typing_extensions import Type

from pydantic import BaseModel

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)


class DirectorBase(BaseModelConfig):
    name: str


class DirectorUpdate(DirectorBase):
    ...


class DirectorCreate(DirectorBase):
    ...


class DirectorResponseBase(DirectorBase):
    id: int


DirectorResponse: Type[BaseModel] = create_response_model(DirectorResponseBase, "DirectorResponse")
