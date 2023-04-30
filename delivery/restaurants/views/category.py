from typing import Annotated, cast

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from delivery.core.depends.auth import require_restaurant
from delivery.core.validation import validate
from delivery.restaurants.form import RestaurantCategoryForm
from delivery.restaurants.schema import (
    BaseRestaurantCategorySchema,
)
from delivery.restaurants.service import RestaurantService

router = APIRouter(prefix="/restaurant/category", tags=["Categories"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def add_category(
    form: RestaurantCategoryForm,
    service: Annotated[RestaurantService, Depends()],
) -> BaseRestaurantCategorySchema:
    validate(
        await service.category_already_exists(form.name),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        ),
    )
    return cast(
        BaseRestaurantCategorySchema,
        await service.add_category(
            form.name,
        ),
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def delete_category(
    category_id: int,
    service: Annotated[RestaurantService, Depends()],
) -> None:
    validate(
        not await service.category_exists_by_id(category_id),
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category Not Found",
        ),
    )
    return await service.delete_category(
        category_id,
    )
