from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.anime import Anime
from app.core.schemas.anime import AnimeCreate, AnimeUpdate
from app.core.controllers.base import CRUDBase
from app.core.controllers.base import ModelType
from app.core.models.rating import Rating


class AnimeCRUD(
    CRUDBase[
        Anime,
        AnimeCreate,
        AnimeUpdate,
    ]
):
    """ Anime CRUD. """

    async def get_chart(self, session: AsyncSession) -> list[ModelType]:
        stmt = (select(self.model)
                .join(Rating)
                .where(Rating.avg_rating is not None and self.model.status == "вышел")
                .order_by(Rating.avg_rating.desc())
                .limit(100)
                )
        result = await session.execute(stmt)
        return result.scalars().all()


anime_crud = AnimeCRUD(Anime)
