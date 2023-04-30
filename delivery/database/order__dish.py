from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delivery.core.models.base import SQLModel

if TYPE_CHECKING:
    from delivery.database import DishModel


class OrderDishAssociation(SQLModel):
    __tablename__ = "order__dish"

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "order.id",
            name="order__dish_order_id_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey(
            "dish.id",
            name="order__dish_dish_id_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    dish: Mapped["DishModel"] = relationship()
    count: Mapped[int]

    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "dish_id",
            name="order__dish_uc",
        ),
    )
