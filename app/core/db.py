from typing_extensions import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.core.settings import settings


class PreBase:
    """Abstract base model."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


Base = declarative_base(
    cls=PreBase,
)

engine = create_async_engine(
    settings.postgres_url, poolclass=AsyncAdaptedQueuePool, pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
