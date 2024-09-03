from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BaseIdName(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.id} - {self.name})"

    def __repr__(self) -> str:
        return str(self)
