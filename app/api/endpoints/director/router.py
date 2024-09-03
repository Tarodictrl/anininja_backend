from typing_extensions import Annotated, Doc

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.director import DirectorResponse, DirectorResponseBase
from app.core.db import get_async_session
from app.core.controllers.director import director_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.base import BaseIdNameFilter

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
