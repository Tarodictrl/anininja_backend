from typing_extensions import Type
from datetime import date

from pydantic import BaseModel, Field

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.base import (
    create_response_model,
)
from app.core.schemas.user import UserPublicResponseBase


class CommentBase(BaseModelConfig):
    message: str
    anime_id: int | None
    parent: int | None


class CommentUpdate(CommentBase):
    ...


class CommentCreate(CommentBase):
    ...


class CommentResponseBase(CommentBase):
    id: int
    user: UserPublicResponseBase | None = Field(default_factory=list)
    comment_date: date


CommentResponse: Type[BaseModel] = create_response_model(CommentResponseBase, "CommentResponse")
