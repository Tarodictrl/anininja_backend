from datetime import date
from typing_extensions import Type

from pydantic import BaseModel, Field

from app.core.schemas.base import BaseModelConfig
from app.core.schemas.anime import AnimeResponseBase
from app.core.schemas.base import (
    create_response_model,
)


class AnimeList(BaseModelConfig):
    status: str
    anime: AnimeResponseBase


class UserListBase(BaseModelConfig):
    anime_id: int
    status: str


class UserListCreate(UserListBase):
    ...


class UserListUpdate(UserListBase):
    ...


class UserBase(BaseModelConfig):
    login: str
    avatar: str | None = None
    registration_date: date | None = Field(alias="registrationDate", default=None)


class UserPublic(UserBase):
    ...


class UserPrivate(UserBase):
    email: str | None = None
    role: str | None = None
    user_list: list[AnimeList] | None = Field(alias="animeList", default_factory=list)
    vk_id: int | None = Field(alias="vkId", default=None)


class UserRegistration(UserPrivate):
    password: str


class UserUpdate(UserBase):
    ...


class UserCreate(UserBase):
    ...


class UserResponseBase(UserBase):
    id: int


class UserPrivateResponseBase(UserPrivate):
    id: int


class UserPublicResponseBase(UserPublic):
    id: int


class LoginSchema(BaseModelConfig):
    login: str
    password: str
    token: str


class RegistrationSchema(LoginSchema):
    email: str


UserResponse: Type[BaseModel] = create_response_model(UserResponseBase, "UserResponse")
