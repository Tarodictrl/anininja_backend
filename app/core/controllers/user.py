from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import User, UserList
from app.core.schemas.user import UserCreate, UserListCreate, UserUpdate, UserListUpdate
from app.core.controllers.base import CRUDBase


class UserCRUD(
    CRUDBase[
        User,
        UserCreate,
        UserUpdate,
    ]
):
    """ User CRUD. """

    async def get_by_creditionals(
        self, session: AsyncSession, login_or_email: str, hashed_password: str,
    ) -> User | None:
        db_obj = await session.scalars(
            select(self.model).where(and_(or_(User.login == login_or_email, User.email == login_or_email), User.password == hashed_password))
        )
        return db_obj.first()

    async def get_profile(
        self, session: AsyncSession, id: int
    ) -> User:
        stmt = (
            select(User)
            .where(User.id == id)
        )
        db_obj = await session.scalars(stmt)
        return db_obj.one()


class UserListCRUD(CRUDBase[UserList, UserListCreate, UserListUpdate]):
    """ User list CRUD. """

    async def get_user_list(
        self, session: AsyncSession, user_id: int
    ) -> list[UserList]:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        db_obj = await session.scalars(stmt)
        return db_obj.one().user_list


user_crud = UserCRUD(User)
user_list_crud = UserListCRUD(UserList)
