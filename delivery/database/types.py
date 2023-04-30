from typing import Annotated, TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

T = TypeVar("T")

pk = Annotated[T, mapped_column(primary_key=True)]

restaurant_fk = Annotated[
    int,
    mapped_column(ForeignKey("restaurant.id"), index=True),
]
category_fk = Annotated[
    int,
    mapped_column(ForeignKey("restaurant_category.id"), index=True),
]
user_fk = Annotated[
    int,
    mapped_column(ForeignKey("user.id"), index=True),
]

city_fk = Annotated[
    int,
    mapped_column(ForeignKey("city.id"), index=True),
]

order_fk = Annotated[
    int,
    mapped_column(ForeignKey("order.id"), index=True),
]

dish_fk = Annotated[
    int,
    mapped_column(ForeignKey("order.id"), index=True),
]
