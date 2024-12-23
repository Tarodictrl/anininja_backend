from typing_extensions import Annotated, Doc

from fastapi import APIRouter, status, Depends, Cookie
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.studio import StudioResponse, StudioResponseBase, StudioUpdate, StudioCreate
from app.core.db import get_async_session
from app.core.controllers.studio import studio_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.base import BaseIdNameFilter
from app.core.security import verify_access_token, validate_permission

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=StudioResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_studios(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filter: BaseIdNameFilter = Depends(),
):

    studios, total = await studio_crud.get_all(session=session, filter=filter)
    return BaseResponseDataMapper(
        studios, total=total,
        limit=filter.limit, offset=filter.offset
    ).result_schema


@router.get(
    "/{id}",
    response_model=StudioResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_by_id_studio(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Studio ID.")],
):

    studio = await studio_crud.get_by_id(session=session, obj_id=id)
    return studio


@router.post(
    "/",
    response_model=StudioResponseBase,
    status_code=status.HTTP_200_OK,
)
async def create_studio(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[StudioCreate, Doc("Studio data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    genre = await studio_crud.create(session=session, obj_in=data)
    return genre


@router.patch(
    "/{id}",
    response_model=StudioResponseBase,
    status_code=status.HTTP_200_OK,
)
async def update_studio(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Studio ID.")],
    data: Annotated[StudioUpdate, Doc("Studio data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    studio = await studio_crud.get_by_id(session=session, obj_id=id)
    if not studio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Studio not found")
    updated_genre = await studio_crud.update(session=session, db_obj=studio, obj_in=data)
    return updated_genre
