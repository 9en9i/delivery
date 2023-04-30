from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from delivery.core.models.base import SQLModel
from delivery.database.types import pk

if TYPE_CHECKING:
    from delivery.database import RestaurantModel, UserModel


class CityModel(SQLModel):
    __tablename__ = "city"

    id: Mapped[pk[int]]
    name: Mapped[str]

    restaurants: Mapped[list["RestaurantModel"]] = relationship(
        back_populates="cities",
        secondary="restaurant__city",
    )

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="city",
    )
