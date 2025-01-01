from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controllers.base import CRUDBase
from app.core.models.comment import Comment
from app.core.schemas.comment import CommentCreate, CommentUpdate


class CommentCRUD(
    CRUDBase[
        Comment,
        CommentCreate,
        CommentUpdate,
    ]
):
    """ Comment CRUD. """
    async def get_all_by_attribute(
        self, attr_name: str, attr_value: str | int, session: AsyncSession
    ) -> list[Comment]:
        attr = getattr(Comment, attr_name)
        db_objs = await session.scalars(select(Comment).where(attr == attr_value).order_by(Comment.comment_date.desc()))
        total_obj = await session.execute(select(func.count(Comment.id)).where(attr == attr_value))
        return db_objs.all(), total_obj.fetchone()[0]


comment_crud = CommentCRUD(Comment)
