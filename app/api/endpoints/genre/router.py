from typing_extensions import Annotated, Doc

from fastapi import APIRouter, status, Depends, Cookie
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.genre import GenreResponse, GenreResponseBase, GenreCreate, GenreUpdate
from app.core.db import get_async_session
from app.core.controllers.genre import genre_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.base import BaseIdNameFilter
from app.core.security import verify_access_token, validate_permission

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_genres(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filter: BaseIdNameFilter = Depends(),
):

    genres, total = await genre_crud.get_all(session=session, filter=filter)
    return BaseResponseDataMapper(
        genres, total=total,
        limit=filter.limit, offset=filter.offset
    ).result_schema


@router.get(
    "/{id}",
    response_model=GenreResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_by_id_genre(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[str, Doc("Genre ID.")],
):

    genre = await genre_crud.get_by_id(session=session, obj_id=id)
    return genre


@router.post(
    "/",
    response_model=GenreResponseBase,
    status_code=status.HTTP_200_OK,
)
async def create_genre(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[GenreCreate, Doc("Genre data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    genre = await genre_crud.create(session=session, obj_in=data)
    return genre


@router.patch(
    "/{id}",
    response_model=GenreResponseBase,
    status_code=status.HTTP_200_OK,
)
async def update_genre(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Genre ID.")],
    data: Annotated[GenreUpdate, Doc("Genre data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    genre = await genre_crud.get_by_id(session=session, obj_id=id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    updated_genre = await genre_crud.update(session=session, db_obj=genre, obj_in=data)
    return updated_genre
