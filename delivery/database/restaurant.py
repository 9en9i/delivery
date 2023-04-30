from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from delivery.core.models.base import SQLModel
from delivery.database.actor import ActorModel
from delivery.database.types import pk, restaurant_fk

if TYPE_CHECKING:
    from delivery.database import CityModel, OrderModel, UserModel


class RestaurantModel(ActorModel):
    __tablename__ = "restaurant"

    name: Mapped[str]
    image: Mapped[str] = mapped_column(default="/images/empty.jpg")
    description: Mapped[str]

    cities: Mapped[list["CityModel"]] = relationship(
        back_populates="restaurants",
        secondary="restaurant__city",
    )
    categories: Mapped[list["RestaurantCategoryModel"]] = relationship(
        back_populates="restaurant",
    )
    dishes: Mapped[list["DishModel"]] = relationship(
        back_populates="restaurant",
    )
    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="restaurant",
    )

    users: Mapped[list["UserModel"]] = relationship(
        secondary="favorite_restaurant",
        back_populates="favorite_restaurants",
    )


class FavoriteRestaurant(SQLModel):
    __tablename__ = "favorite_restaurant"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", name="fk_user_id"),
        primary_key=True,
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id", name="fk_restaurant_id"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "restaurant_id",
            name="user__restaurant_uc",
        ),
    )


class RestaurantCategoryModel(SQLModel):
    __tablename__ = "restaurant_category"
    id: Mapped[pk[int]]
    name: Mapped[str]
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "restaurant.id",
            name="category_restaurant_fk",
            ondelete="CASCADE",
        ),
        index=True,
    )

    dishes: Mapped[list["DishModel"]] = relationship(
        back_populates="category",
    )

    restaurant: Mapped["RestaurantModel"] = relationship(
        back_populates="categories",
    )

    __table_args__ = (UniqueConstraint("name", "restaurant_id"),)


class DishModel(SQLModel):
    __tablename__ = "dish"
    id: Mapped[pk[int]]

    name: Mapped[str]
    image: Mapped[str] = mapped_column(default="/images/empty.jpg")
    price: Mapped[float]
    description: Mapped[str]
    restaurant_id: Mapped[restaurant_fk]
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "restaurant_category.id",
            name="dish_category_fk",
            ondelete="CASCADE",
        ),
        index=True,
    )

    restaurant: Mapped["RestaurantModel"] = relationship(
        back_populates="dishes",
    )
    category: Mapped["RestaurantCategoryModel"] = relationship(
        back_populates="dishes",
    )

    __table_args__ = (
        UniqueConstraint("name", "restaurant_id", name="name_restaurant_uc"),
    )
