from fastapi import APIRouter, Depends, Body
from starlette import status

from delivery.core.depends.auth import (
    require_user,
    require_restaurant,
    InjectMaybeUser,
    InjectActor,
)
from delivery.core.enums.order_status import OrderStatus
from delivery.orders.exceptions import OrderDoesNotExist
from delivery.orders.forms import OrderForm
from delivery.orders.schemas import OrderSchema
from delivery.orders.service import InjectOrderService
from delivery.orders.validations import InjectOrderValidations
from delivery.restaurants.exceptions import RestaurantDoesNotExist, DishesDoesNotExist

router = APIRouter(prefix="/order", tags=["Order"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_user),
    ],
)
async def create_order(
    form: OrderForm,
    validation: InjectOrderValidations,
    service: InjectOrderService,
) -> None:
    if await validation.restaurant_not_exists(form.restaurant_id):
        raise RestaurantDoesNotExist

    if await validation.dishes_not_exists(form.restaurant_id, form.dish_ids):
        raise DishesDoesNotExist

    await service.create_order(form)


@router.get("/")
async def get_orders(
    actor: InjectActor,
    service: InjectOrderService,
) -> list[OrderSchema]:
    _, actor_type = actor
    orders = await service.get_orders(actor_type)

    return OrderSchema.to_schemas(orders)


@router.patch("/{order_id}", dependencies=[Depends(require_restaurant)])
async def update_orders(
    order_id: int,
    service: InjectOrderService,
    validation: InjectOrderValidations,
    status_: OrderStatus = Body(alias="status", embed=True),
) -> None:
    if await validation.order_not_exists(order_id):
        raise OrderDoesNotExist()

    await service.update_order(order_id, status_)
