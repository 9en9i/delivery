import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from delivery.core.enums.order_status import OrderStatus
from delivery.core.models.base import SQLModel
from delivery.database.types import pk, restaurant_fk, user_fk

if TYPE_CHECKING:
    from delivery.database import (
        RestaurantModel,
        UserModel,
        DishModel,
        OrderDishAssociation,
    )


class OrderModel(SQLModel):
    __tablename__ = "order"

    id: Mapped[pk[int]]
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    delivery_address: Mapped[str]

    restaurant_id: Mapped[restaurant_fk]
    restaurant: Mapped["RestaurantModel"] = relationship(
        back_populates="orders",
    )

    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(
        back_populates="orders",
    )

    dishes: Mapped[list["DishModel"]] = relationship(
        secondary="order__dish",
    )

    dish_associations: Mapped[list["OrderDishAssociation"]] = relationship(
        viewonly=True
    )
