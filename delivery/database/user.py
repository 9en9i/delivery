from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from delivery.database.actor import ActorModel
from delivery.database.types import city_fk

if TYPE_CHECKING:
    from delivery.database import CityModel, OrderModel, RestaurantModel


class UserModel(ActorModel):
    __tablename__ = "user"
    first_name: Mapped[str]
    last_name: Mapped[str]
    city_id: Mapped[city_fk]

    city: Mapped["CityModel"] = relationship(
        back_populates="users",
    )
    orders: Mapped["OrderModel"] = relationship(
        back_populates="user",
    )

    favorite_restaurants: Mapped["RestaurantModel"] = relationship(
        secondary="favorite_restaurant",
        back_populates="users",
    )
