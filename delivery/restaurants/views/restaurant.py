from typing import cast

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
)

from delivery.auth.exceptions import EmailAlreadyRegistered
from delivery.cities.exceptions import InvalidCities
from delivery.core.depends.auth import require_user, require_restaurant
from delivery.restaurants.exceptions import (
    RestaurantNotFound,
    RestaurantCantFavoriteRestaurant,
    RestaurantDoesNotExist,
    RestaurantAlreadyFavorite,
    RestaurantCantUnavoriteRestaurant,
    RestaurantNotFavorite,
)
from delivery.restaurants.form import JoinRestaurantForm
from delivery.restaurants.schema import (
    RestaurantSchema,
    RestaurantWithMenuSchema,
    CreateRestaurantSchema,
)
from delivery.restaurants.service import InjectRestaurantService
from delivery.restaurants.validations import (
    InjectRestaurantValidations,
)

router = APIRouter(prefix="/restaurant", tags=["Restaurants"])


@router.get("")
async def read_restaurants(
    service: InjectRestaurantService,
    city_id: int,
    offset: int = 0,
    limit: int = 100,
) -> list[RestaurantSchema]:
    restaurants = await service.get_all(
        city_id=city_id,
        offset=offset,
        limit=limit,
    )
    return RestaurantSchema.to_schemas(restaurants)


@router.get("/{restaurant_id}")
async def read_restaurant(
    service: InjectRestaurantService,
    restaurant_id: int,
    city_id: int,
) -> RestaurantWithMenuSchema:
    restaurant = await service.get_restaurant_with_menu(restaurant_id, city_id)
    if not restaurant:
        raise RestaurantNotFound
    return RestaurantWithMenuSchema.to_schema(restaurant)


@router.post("/join", status_code=status.HTTP_201_CREATED)
async def join(
    form: JoinRestaurantForm,
    service: InjectRestaurantService,
) -> CreateRestaurantSchema:
    if await service.email_already_exists(form.email):
        raise EmailAlreadyRegistered
    if await service.cities_are_not_valid(form.cities):
        raise InvalidCities

    restaurant = await service.create_restaurant(
        email=form.email,
        password=form.password,
        name=form.name,
        description=form.description,
        cities=form.cities,
        open_time=form.open_time,
        close_time=form.close_time,
    )
    return CreateRestaurantSchema.to_schema(restaurant)


@router.post(
    "/add_image",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[
        Depends(require_restaurant),
    ],
)
async def add_image(
    image: UploadFile,
    service: InjectRestaurantService,
) -> CreateRestaurantSchema:
    return cast(RestaurantSchema, await service.add_image(image))


@router.post(
    "/{restaurant_id}/favorite",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_user),
    ],
)
async def favorite_restaurant(
    restaurant_id: int,
    service: InjectRestaurantService,
    validator: InjectRestaurantValidations,
) -> None:
    if await validator.is_restaurant():
        raise RestaurantCantFavoriteRestaurant
    if not await service.restaurant_exists(restaurant_id):
        raise RestaurantDoesNotExist
    if await service.restaurant_already_favorite(restaurant_id):
        raise RestaurantAlreadyFavorite

    await service.add_favorite_restaurant(restaurant_id)


@router.delete(
    "/{restaurant_id}/favorite",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[
        Depends(require_user),
    ],
)
async def delete_favorite_restaurant(
    restaurant_id: int,
    service: InjectRestaurantService,
    validator: InjectRestaurantValidations,
) -> None:
    if await validator.is_restaurant():
        raise RestaurantCantUnavoriteRestaurant
    if not await service.restaurant_exists(restaurant_id):
        raise RestaurantDoesNotExist
    if not await service.restaurant_already_favorite(restaurant_id):
        raise RestaurantNotFavorite

    await service.delete_favorite_restaurant(restaurant_id)
