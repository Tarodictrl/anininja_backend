"""
This module contains a generic class for CRUD operations.
"""

from dataclasses import dataclass
from typing_extensions import Any, Generic, Type, TypeVar

from sqlalchemy import select, func, text, literal_column
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@dataclass
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic class for CRUD operations.

    Args:
    - ModelType: The type of the model.
    - CreateSchemaType: The type of the schema for creating objects.
    - UpdateSchemaType: The type of the schema for updating objects.
    """

    model: Type[ModelType]

    async def get_all(self, session: AsyncSession, filter: PydanticModel) -> list[ModelType]:
        """
        Get all objects of the specified model.

        Args:
        - session: The database session.

        Returns:
        - A list of objects of the specified model.
        """
        stmt = await self.filter_constructor(select(self.model), filter)
        db_objs = await session.scalars(stmt)
        total_stmt = await self.filter_constructor(select(func.count(self.model.id)),
                                                   filter, use_limit=False, use_offset=False)
        total_obj = await session.execute(total_stmt)
        return db_objs.all(), total_obj.fetchone()[0]

    async def get_all_with_pagination(
        self, pagination: PydanticModel, session: AsyncSession
    ) -> list[ModelType]:
        """
        Get all objects of the specified model with pagination.

        Args:
        - pagination: The pagination schema.
        - session: The database session.

        Returns:
        - A list of objects of the specified model.
        """
        query = await session.scalars(
            select(self.model)
            .offset((pagination.page - 1) * pagination.page_size)
            .limit(pagination.page_size)
        )
        return query.all()

    async def get_by_id(self, obj_id: int, session: AsyncSession) -> ModelType | None:
        """
        Get an object by its ID.

        Args:
        - obj_id: The ID of the object.
        - session: The database session.

        Returns:
        - The object with the specified ID, or None if not found.
        """
        return await session.get(self.model, obj_id)

    async def get_by_double_primary_key(
        self, obj_pk_one: int, obj_pk_two: str, session: AsyncSession
    ) -> ModelType:
        """
        Get an object its two primary keys.

        Args:
        - obj_pk_one: The first primary key value.
        - obj_pk_two: The second primary key value.
        - session (AsyncSession): The database session to use for the query.

        Returns:
        - ModelType: The retrieved object or None if no object is found.
        """
        return await session.get(self.model, (obj_pk_one, obj_pk_two))

    async def get_by_attribute(
        self, attr_name: str, attr_value: str | int, session: AsyncSession
    ) -> ModelType | None:
        """
        Get an object by a specific attribute.

        Args:
        - attr_name (str): The name of the attribute to filter by.
        - attr_value (str): The value of the attribute to filter by.
        - session (AsyncSession): The async session to use for the database query.

        Returns:
        - The database object that matches the specified attribute and value, or None if not found.
        """
        attr = getattr(self.model, attr_name)
        db_obj: ModelType | None = await session.scalars(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.first()

    async def get_all_by_attribute(
        self, attr_name: str, attr_value: str | int, session: AsyncSession
    ) -> list[ModelType]:
        """
        Get all objects by a specific attribute.

        Args:
        - attr_name (str): The name of the attribute to filter by.
        - attr_value (str): The value of the attribute to filter by.
        - session (AsyncSession): The async session to use for the database query.

        Returns:
        - The database objects that match the specified attribute and value.
        """
        attr = getattr(self.model, attr_name)
        db_objs = await session.scalars(select(self.model).where(attr == attr_value))
        return db_objs.all()

    async def create(
        self, obj_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        """
        Create a new object.

        Args:
        - obj_in: The data for the new object.
        - session: The database session.

        Returns:
        - The created object.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        session: AsyncSession,
    ) -> ModelType:
        """
        Update an existing object.

        Args:
        - db_obj: The object to be updated.
        - obj_in: The data for the update.
        - session: The database session.

        Returns:
        - The updated object.
        """
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
        """
        Remove an existing object.

        Args:
        - db_obj: The object to be removed.
        - session: The database session.

        Returns:
        - The removed object.
        """
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
