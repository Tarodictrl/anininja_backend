"""
This module contains a generic class for CRUD operations.
"""

from dataclasses import dataclass
from typing_extensions import Any, Generic, Type, TypeVar

from sqlalchemy import select, func, text, literal_column, desc, asc
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.core.db import Base
from app.core.models.rating import Rating

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@dataclass
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    model: Type[ModelType]

    async def get_all(self, session: AsyncSession, filter: PydanticModel) -> list[ModelType]:
        stmt = await self.filter_constructor(select(self.model), filter)
        stmt = await self.order_by_constructor(stmt, filter)
        db_objs = await session.scalars(stmt)
        total_stmt = await self.filter_constructor(select(func.count(self.model.id)),
                                                   filter, use_limit=False, use_offset=False)
        total_obj = await session.execute(total_stmt)
        return db_objs.all(), total_obj.fetchone()[0]

    async def get_all_with_pagination(
        self, pagination: PydanticModel, session: AsyncSession
    ) -> list[ModelType]:
        query = await session.scalars(
            select(self.model)
            .offset((pagination.page - 1) * pagination.page_size)
            .limit(pagination.page_size)
        )
        return query.all()

    async def get_by_id(self, obj_id: int, session: AsyncSession) -> ModelType | None:
        return await session.get(self.model, obj_id)

    async def get_by_attribute(
        self, attr_name: str, attr_value: str | int, session: AsyncSession
    ) -> ModelType | None:
        attr = getattr(self.model, attr_name)
        db_obj: ModelType | None = await session.scalars(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.first()

    async def get_all_by_attribute(
        self, attr_name: str, attr_value: str | int, session: AsyncSession
    ) -> list[ModelType]:
        attr = getattr(self.model, attr_name)
        db_objs = await session.scalars(select(self.model).where(attr == attr_value))
        total_obj = await session.execute(select(func.count(self.model.id)).where(attr == attr_value))
        return db_objs.all(), total_obj.fetchone()[0]

    async def create(
        self, obj_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        session: AsyncSession,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True, by_alias=False)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: ModelType, session: AsyncSession) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def filter_constructor(self, stmt: Query, filter: PydanticModel,
                                 use_limit: bool = True, use_offset: bool = True) -> Query:
        for key, value in filter:
            if hasattr(self.model, key):
                if isinstance(value, int):
                    stmt = stmt.where(literal_column(key) == value)
                elif isinstance(value, str):
                    stmt = stmt.where(text(f"{key} ilike '%{value}%'"))
            elif key == "limit" and use_limit:
                stmt = stmt.limit(value)
            elif key == "offset" and use_offset:
                stmt = stmt.offset(value)
        return stmt

    async def order_by_constructor(self, stmt: Query, filter: PydanticModel) -> Query:
        order_by = filter.order_by
        direction = filter.direction
        if hasattr(self.model, order_by):
            stmt = stmt.order_by(asc(literal_column(order_by) if direction == "asc" else desc(literal_column(order_by))))
        else:
            if order_by == "relevance":
                stmt = stmt.join(Rating).order_by(Rating.avg_rating.desc() if direction == "asc" else Rating.avg_rating).where(Rating.avg_rating is not None)
        return stmt
