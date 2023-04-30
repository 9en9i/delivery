import datetime

from pydantic import BaseModel, Field, validator


class DishDTO(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str


class RestaurantCategoryDTO(BaseModel):
    id: int
    name: str
    dishes: list[DishDTO]

    @validator("dishes", pre=True)
    def not_null_dishes(cls, v: list | None) -> list:
        return v or []


class RestaurantDTO(BaseModel):
    id: int
    name: str
    image: str
    description: str
    opening_time: datetime.time
    closing_time: datetime.time
    is_favorite: bool | None


class RestaurantWithMenuDTO(RestaurantDTO):
    categories: list[RestaurantCategoryDTO] = Field(default_factory=list)

    @validator("categories", pre=True)
    def not_null_category(cls, v: list | None) -> list:
        return v or []
