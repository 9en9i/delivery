from collections.abc import Sequence
from typing import Annotated, cast

from fastapi import Depends

from delivery.core.depends.auth import InjectMaybeUser
from delivery.core.depends.db import InjectSession
from delivery.core.enums.actors import ActorEnum
from delivery.core.enums.order_status import OrderStatus
from delivery.database import RestaurantModel, UserModel, OrderModel
from delivery.orders.dto import OrderDTO
from delivery.orders.forms import OrderForm
from delivery.orders.repository import InjectOrderRepository


class OrderService:
    def __init__(
        self,
        session: InjectSession,
        order_repository: InjectOrderRepository,
        user: InjectMaybeUser,
    ):
        self.session = session
        self.user = user
        self.order_repository = order_repository

    async def create_order(self, form: OrderForm) -> OrderModel:
        order = self.order_repository.create_order(
            self.user,
            form.restaurant_id,
            form.address,
        )
        await self.session.flush()
        for i in form.dishes:
            await self.order_repository.add_dishes(order.id, i)

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update_order(self, order_id: int, status: OrderStatus) -> None:
        if order := await self.order_repository.update_order(
            order_id, status, self.user
        ):
            await self.session.commit()
            return order
        return None

    async def get_orders(self, actor: ActorEnum) -> Sequence[OrderDTO]:
        orders = await self.order_repository.get_orders(
            actor, cast(RestaurantModel | UserModel, self.user)
        )
        data = []
        for order in orders:
            temp = {
                "id": order.id,
                "status": order.status,
                "time": order.time,
                "delivery_address": order.delivery_address,
                "dishes": [],
            }
            for association in order.dish_associations:
                temp["dishes"].append(
                    {
                        "id": association.dish.id,
                        "name": association.dish.name,
                        "price": association.dish.price,
                        "image": association.dish.image,
                        "count": association.count,
                    }
                )
            data.append(OrderDTO(**temp))
        return data

    async def order_exists(self, order_id: int) -> bool:
        return await self.order_repository.order_exists(order_id)


InjectOrderService = Annotated[OrderService, Depends()]
