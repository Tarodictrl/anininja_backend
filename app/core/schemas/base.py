from typing_extensions import TypeVar

from pydantic import BaseModel, create_model, Field, ConfigDict

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class BaseModelConfig(BaseModel):
    model_config: ConfigDict = ConfigDict(
        strict=True,
        populate_by_name=True,
        from_attributes=True,
        str_max_length=5000,
        extra="forbid",
    )


def create_response_model(schema: PydanticModel, model_name: str) -> PydanticModel:
    """
    Create response model with dynamic items and items count.
    """
    return create_model(
        model_name,
        responses=(list[schema], ...),
        total=(int, Field(...)),
        limit=(int, Field(...)),
        offset=(int, Field(...)),
        __base__=BaseModelConfig,
        __module__="",
    )
