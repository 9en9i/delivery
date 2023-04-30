import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from delivery.core.models.base import SQLModel
from delivery.database.types import city_fk, restaurant_fk


class RestaurantCityAssociation(SQLModel):
    __tablename__ = "restaurant__city"

    restaurant_id: Mapped[restaurant_fk] = mapped_column(primary_key=True)
    city_id: Mapped[city_fk] = mapped_column(primary_key=True)
    opening_time: Mapped[datetime.time]
    closing_time: Mapped[datetime.time]

    __table_args__ = (
        UniqueConstraint("restaurant_id", "city_id", name="restaurant__city__uc"),
    )
