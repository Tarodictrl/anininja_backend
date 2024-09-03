from typing_extensions import Annotated, Doc

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.studio import StudioResponse, StudioResponseBase
from app.core.db import get_async_session
from app.core.controllers.studio import studio_crud
from app.core.mapper import BaseResponseDataMapper
from app.core.filters.base import BaseIdNameFilter

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
    id: Annotated[int, Doc("Genre ID.")],
):

    studio = await studio_crud.get_by_id(session=session, obj_id=id)
    return studio
