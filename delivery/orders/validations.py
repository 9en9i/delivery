from typing import Annotated

from fastapi import Depends

from delivery.orders.service import InjectOrderService
from delivery.restaurants.service import InjectRestaurantService


class OrderValidations:
    def __init__(
        self,
        restaurant_service: InjectRestaurantService,
        order_service: InjectOrderService,
    ):
        self.restaurant_service = restaurant_service
        self.order_service = order_service

    async def restaurant_not_exists(self, restaurant_id: int) -> bool:
        return not await self.restaurant_service.restaurant_exists(restaurant_id)

    async def dishes_not_exists(self, restaurant_id: int, dish_ids: list[int]) -> bool:
        return not await self.restaurant_service.dishes_exists(dish_ids, restaurant_id)

    async def order_not_exists(self, order_id: int) -> bool:
        return not await self.order_service.order_exists(order_id)


InjectOrderValidations = Annotated[OrderValidations, Depends()]
