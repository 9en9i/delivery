from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import overload, Annotated

from fastapi import Depends
from sqlalchemy import update, select
from sqlalchemy.orm import joinedload

from delivery.core.controllers.base import BaseController
from delivery.core.depends.db import InjectSession
from delivery.core.enums.actors import ActorEnum
from delivery.core.enums.order_status import OrderStatus
from delivery.database import (
    OrderModel,
    UserModel,
    OrderDishAssociation,
    RestaurantModel,
)
from delivery.orders.forms import OrderDishForm


class OrderRepository(BaseController):
    model = OrderModel

    def __init__(self, db: InjectSession):
        super().__init__(db)

    def create_order(
        self,
        user: UserModel,
        restaurant_id: int,
        address: str,
    ):
        order = OrderModel(
            user_id=user.id,
            restaurant_id=restaurant_id,
            delivery_address=address,
            time=datetime.now() + timedelta(hours=1),
        )
        self.session.add(order)
        return order

    async def add_dishes(self, order_id: int, dish: OrderDishForm):
        self.session.add(
            OrderDishAssociation(
                order_id=order_id,
                dish_id=dish.dish_id,
                count=dish.amount,
            )
        )

    async def update_order(
        self,
        order_id: int,
        status: OrderStatus,
        restaurant: RestaurantModel,
    ) -> OrderModel | None:
        stmt = (
            update(OrderModel)
            .where(
                OrderModel.id == order_id,
                OrderModel.restaurant_id == restaurant.id,
            )
            .values(status=status)
            .returning(OrderModel.id)
        )
        r = await self.session.execute(stmt)
        return r.scalar()

    @overload
    async def get_orders(
        self,
        actor: ActorEnum,
        user: UserModel,
    ) -> Sequence[OrderModel]:
        ...

    @overload
    async def get_orders(
        self,
        actor: ActorEnum,
        user: RestaurantModel,
    ) -> Sequence[OrderModel]:
        ...

    async def get_orders(
        self,
        actor,
        user,
    ):
        stmt = select(OrderModel).options(
            joinedload(OrderModel.dishes),
            joinedload(OrderModel.dish_associations),
        )
        if actor is ActorEnum.RESTAURANT:
            result = await self.session.scalars(
                stmt.where(OrderModel.restaurant_id == user.id)
            )
        else:
            result = await self.session.scalars(
                stmt.where(OrderModel.user_id == user.id)
            )
        return result.unique().all()

    async def order_exists(self, order_id: int) -> bool:
        return (
            await self.session.scalar(
                select(OrderModel.id).where(OrderModel.id == order_id)
            )
            is not None
        )


InjectOrderRepository = Annotated[OrderRepository, Depends()]
