from dataclasses import dataclass
from typing_extensions import Generic

from app.core.schemas.base import PydanticModel


@dataclass
class BaseResponseDataMapper:
    """
    A generic class for mapping the response data to a Pydantic schema.
    """

    data: list
    limit: int = 100
    offset: int = 0
    total: int = 0

    @property
    def result_schema(self) -> Generic[PydanticModel]:
        return dict(
            responses=self.data,
            total=self.total,
            limit=self.limit,
            offset=self.offset,
        )
