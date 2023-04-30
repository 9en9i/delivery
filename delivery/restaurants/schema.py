import datetime

from pydantic import validator

from delivery.core.schema import BaseSchema
from delivery.settings import settings
from delivery.users.schema import TokenSchema  # noqa: F401


class RestaurantCitySchema(BaseSchema):
    id: int
    name: str


class CreateRestaurantSchema(BaseSchema):
    id: int
    name: str
    image: str
    description: str

    @validator("image")
    def absolute_path(cls, v) -> str:
        return f"{settings.MEDIA_URL}{v}" if v else None


class RestaurantSchema(CreateRestaurantSchema):
    is_favorite: bool | None
    opening_time: datetime.time
    closing_time: datetime.time


class DishSchema(BaseSchema):
    id: int
    name: str
    description: str
    price: float
    image: str | None
    # category_id: int

    @validator("image")
    def absolute_path(cls, v) -> str:
        return f"{settings.MEDIA_URL}{v}" if v else None


class BaseRestaurantCategorySchema(BaseSchema):
    id: int
    name: str


class RestaurantCategorySchema(BaseRestaurantCategorySchema):
    dishes: list[DishSchema] | None


class RestaurantWithMenuSchema(RestaurantSchema):
    categories: list[RestaurantCategorySchema]
