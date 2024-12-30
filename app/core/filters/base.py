from typing_extensions import Literal

from pydantic import Field
from fastapi import Query

from app.core.schemas.base import BaseModelConfig


class BaseFilter(BaseModelConfig):
    limit: int = Field(Query(default=100, description="limit", ge=0, le=100))
    offset: int = Field(Query(default=0, description="offset"))


class BaseIdNameFilter(BaseFilter):
    id: int | None = Field(Query(None, description="id"))
    name: str | None = Field(Query(None, description="name"))
    order_by: Literal["id", "name"] | None = Field(Query(default="id", description="order_by"))
    direction: Literal["asc", "desc"] | None = Field(Query(default="asc", description="direction"))
