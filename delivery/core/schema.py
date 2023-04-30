from typing import cast, Self

from pydantic.main import BaseModel


class BaseSchema(BaseModel):
    @classmethod
    def to_schema(cls, value) -> Self:
        return cast(cls, value)

    @classmethod
    def to_schemas(cls, value) -> list[Self]:
        return cast(list[cls], value)

    class Config:
        orm_mode = True
