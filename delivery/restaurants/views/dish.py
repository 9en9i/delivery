from typing import Annotated, cast

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
)

from delivery.core.depends.auth import require_restaurant
from delivery.core.enums.actors import ActorEnum
from delivery.core.validation import validate
from delivery.restaurants.form import (
    RestaurantDishForm,
)
from delivery.restaurants.schema import DishSchema
from delivery.restaurants.service import RestaurantService, InjectRestaurantService

router = APIRouter(prefix="/restaurant/dish", tags=["Dish"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def add_dish(
    form: RestaurantDishForm,
    service: InjectRestaurantService,
) -> DishSchema:
    validate(
        not await service.category_exists_by_id(form.category_id),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not exists",
        ),
    )
    validate(
        await service.dish_already_exists(form.name),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dish already exists",
        ),
    )
    return DishSchema.to_schema(
        await service.create_dish(
            form.category_id,
            form.name,
            form.description,
            form.price,
        ),
    )


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def delete_dish(
    dish_id: int,
    service: InjectRestaurantService,
) -> None:
    validate(
        not await service.dish_exists_by_id(dish_id),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dish not exists",
        ),
    )
    return await service.delete_dish(dish_id)


@router.post(
    "/{dish_id}/add_image",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def add_image(
    dish_id: int,
    image: UploadFile,
    service: InjectRestaurantService,
) -> DishSchema:
    validate(
        not await service.dish_exists_by_id(dish_id),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dish not exists",
        ),
    )
    return cast(DishSchema, await service.add_image_dish(dish_id, image))
