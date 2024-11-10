from typing_extensions import Literal

from pydantic import Field
from fastapi import Query

from app.core.filters.base import BaseIdNameFilter


class AnimeFilter(BaseIdNameFilter):
    status: str | None = Field(Query(default=None, description="status"))
    count_series: int | None = Field(Query(default=None, description="count of series"))
    year: int | None = Field(Query(default=None, description="year", ge=1900))
    season: int | None = Field(Query(default=None, description="season", ge=1, le=4))
    type: str | None = Field(Query(default=None, description="type"))
    age: str | None = Field(Query(default=None, description="age"))
    url: str | None = Field(Query(default=None, description="url"))
    order_by: Literal["relevance", "year", "name"] | None = Field(Query(default="relevance", description="order_by"))
    direction: Literal["asc", "desc"] | None = Field(Query(default="asc", description="direction"))
