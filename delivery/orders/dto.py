from datetime import datetime

from pydantic import BaseModel


class OrderDishDTO(BaseModel):
    name: str
    price: int

    image: str
    count: int


class OrderDTO(BaseModel):
    id: int
    status: str
    delivery_address: str
    time: datetime
    dishes: list[OrderDishDTO]
