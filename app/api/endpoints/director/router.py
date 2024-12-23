from typing_extensions import Annotated, Doc

from fastapi import APIRouter, status, Depends, Cookie
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.director import DirectorResponse, DirectorResponseBase, DirectorCreate, DirectorUpdate
from app.core.db import get_async_session
from app.core.controllers.director import director_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.base import BaseIdNameFilter
from app.core.security import verify_access_token, validate_permission

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=DirectorResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_directors(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filter: BaseIdNameFilter = Depends(),
):
    directors, total = await director_crud.get_all(session=session, filter=filter)
    return BaseResponseDataMapper(
        directors, total=total,
        limit=filter.limit, offset=filter.offset
    ).result_schema


@router.get(
    "/{id}",
    response_model=DirectorResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_by_id_director(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Director ID.")],
):

    director = await director_crud.get_by_id(session=session, obj_id=id)
    return director


@router.post(
    "/",
    response_model=DirectorResponseBase,
    status_code=status.HTTP_200_OK,
)
async def create_director(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[DirectorCreate, Doc("Director data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    director = await director_crud.create(session=session, obj_in=data)
    return director


@router.patch(
    "/{id}",
    response_model=DirectorResponseBase,
    status_code=status.HTTP_200_OK,
)
async def update_director(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int, Doc("Director ID.")],
    data: Annotated[DirectorUpdate, Doc("Director data.")],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    await validate_permission(user_id, "admin", session)
    director = await director_crud.get_by_id(session=session, obj_id=id)
    if not director:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")
    updated_director = await director_crud.update(session=session, db_obj=director, obj_in=data)
    return updated_director
