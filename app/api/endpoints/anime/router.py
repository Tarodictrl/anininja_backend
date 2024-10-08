from typing_extensions import Annotated, Doc
from random import randint

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.anime import AnimeResponse, AnimeResponseBase
from app.core.db import get_async_session
from app.core.controllers.anime import anime_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.anime import AnimeFilter

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=AnimeResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_anime(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filter: AnimeFilter = Depends()
):

    anime, total = await anime_crud.get_all(session=session, filter=filter)
    return BaseResponseDataMapper(anime, total=total).result_schema


@router.get(
    "/random",
    response_model=AnimeResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_random_anime(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    obj_id = randint(1, 8500)
    anime = await anime_crud.get_by_id(session=session, obj_id=obj_id)
    return anime


@router.get(
    "/chart",
    response_model=list[AnimeResponseBase],
    status_code=status.HTTP_200_OK,
)
async def get_chart_anime(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    anime = await anime_crud.get_chart(session=session)
    return anime


@router.get(
    "/{id}",
    response_model=AnimeResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_by_id_anime(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Anime ID.")],
):
    anime = await anime_crud.get_by_id(session=session, obj_id=id)
    return anime
