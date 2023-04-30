import datetime

from pydantic import BaseModel, Field, EmailStr


class JoinRestaurantForm(BaseModel):
    name: str
    email: EmailStr
    password: str
    description: str
    cities: set[int]
    open_time: datetime.time = Field(example="10:00:00")
    close_time: datetime.time = Field(example="23:00:00")


class RestaurantCategoryForm(BaseModel):
    name: str


class RestaurantDishForm(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
