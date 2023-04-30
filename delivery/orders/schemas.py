from datetime import datetime

from pydantic import validator

from delivery.core.schema import BaseSchema
from delivery.settings import settings


class OrderDishSchema(BaseSchema):
    name: str
    price: int

    image: str
    count: int

    @validator("image")
    def image_validator(cls, value: str) -> str:
        return f"{settings.MEDIA_URL}{value}"

    # @property
    # def image(self) -> HttpUrl:
    #     return f"{settings.MEDIA_URL}/{self.image}"


class OrderSchema(BaseSchema):
    id: int
    status: str
    delivery_address: str
    time: datetime
    dishes: list[OrderDishSchema]
    # price: int
