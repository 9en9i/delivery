import datetime
import uuid
from typing import Annotated, TypeAlias

from fastapi import Depends, UploadFile
from minio import Minio

from delivery.auth.service import ActorService
from delivery.cities.controller import InjectCityRepository
from delivery.core.depends.auth import InjectMaybeUser
from delivery.core.depends.db import InjectSession, InjectStorage
from delivery.core.enums.actors import ActorEnum
from delivery.core.required_user import required_user
from delivery.database import (
    RestaurantModel,
    UserModel,
    RestaurantCategoryModel,
    DishModel,
)
from delivery.restaurants.controller import InjectRestaurantRepository
from delivery.restaurants.dto import RestaurantDTO, RestaurantWithMenuDTO


class RestaurantService(ActorService):
    def __init__(
        self,
        session: InjectSession,
        restaurant_repository: InjectRestaurantRepository,
        city_repository: InjectCityRepository,
        storage: InjectStorage,
        user: InjectMaybeUser,
    ):
        self.restaurant_repository = restaurant_repository
        self.city_repository = city_repository
        self.storage = storage
        self.session = session
        self.user = user

    async def get_all(
        self,
        city_id: int,
        limit: int | None,
        offset: int | None,
    ) -> list[RestaurantDTO]:
        restaurants = []
        for restaurant in await self.restaurant_repository.get_all(
            city_id,
            self.user,
            limit=limit,
            offset=offset,
        ):
            restaurants.append(RestaurantDTO(**restaurant))
        return restaurants

    async def auth(self, email: str, password: str) -> RestaurantModel | None:
        return await self.restaurant_repository.get_by_email(email)

    async def email_already_exists(self, email) -> bool:
        return await self.restaurant_repository.exists(email)

    async def cities_are_not_valid(self, cities: set[int]) -> bool:
        return len(await self.city_repository.get_by_ids(cities)) != len(cities)

    async def create_restaurant(
        self,
        email: str,
        name: str,
        description: str,
        password: str,
        cities: set[int],
        open_time: datetime.time,
        close_time: datetime.time,
    ) -> RestaurantWithMenuDTO:
        model_ = await self.restaurant_repository.create(
            name=name,
            description=description,
            email=email,
            password=password,
            cities=cities,
        )
        self.session.add(model_)
        cities = await self.city_repository.get_by_ids(cities)
        await self.restaurant_repository.add_cities(
            model_.id,
            cities,
            open_time=open_time,
            close_time=close_time,
        )
        await self.session.commit()
        await self.session.refresh(model_)
        return model_

    @required_user
    async def add_image(self, image: UploadFile) -> RestaurantModel:
        file_name = f"{self.user.id}/{uuid.uuid4()}"
        self.storage.put_object(
            "images",
            file_name,
            image.file,
            image.size,
            image.content_type,
        )
        self.user.image = f"/images/{file_name}"
        await self.session.commit()
        await self.session.refresh(self.user)
        return self.user

    @required_user
    async def add_image_dish(self, dish_id: int, image: UploadFile) -> DishModel:
        dish = await self.restaurant_repository.get_dish_by_id(self.user, dish_id)
        file_name = f"{self.user.id}/dishes/{dish_id}/{uuid.uuid4()}"
        self.storage.put_object(
            "images",
            file_name,
            image.file,
            image.size,
            image.content_type,
        )
        dish.image = f"/images/{file_name}"
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    @required_user
    async def category_exists_by_id(self, category_id: int) -> bool:
        return await self.restaurant_repository.category_exists_by_id(
            self.user, category_id
        )

    @required_user
    async def dish_already_exists(self, name: str) -> bool:
        return await self.restaurant_repository.dish_already_exists(self.user, name)

    @required_user
    async def dish_exists_by_id(self, dish_id: int) -> bool:
        return await self.restaurant_repository.dish_exists(self.user, dish_id)

    @required_user
    async def delete_dish(self, dish_id: int) -> None:
        await self.restaurant_repository.delete_dish(dish_id)
        await self.session.commit()
        return

    @required_user
    async def category_already_exists(self, name: str) -> bool:
        return await self.restaurant_repository.category_exists(self.user, name)

    @required_user
    async def create_dish(
        self,
        category_id: int,
        name: str,
        description: str,
        price: float,
    ) -> DishModel:
        dish = await self.restaurant_repository.create_dish(
            self.user,
            category_id,
            name,
            description,
            price,
        )
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    # @required_user
    # async def category_not_found(self, category_id: int) -> bool:
    #     return await self.restaurant_repository.category_exists_by_id(
    #         self.user, category_id
    #     )

    @required_user
    async def add_category(self, name: str) -> RestaurantCategoryModel:
        category = await self.restaurant_repository.add_category(self.user, name)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    @required_user
    async def delete_category(self, category_id: int) -> None:
        await self.restaurant_repository.delete_category(self.user, category_id)
        await self.session.commit()

    async def get_restaurant_with_menu(
        self,
        restaurant_id: int,
        city_id: int,
    ) -> RestaurantWithMenuDTO | None:
        restaurant = await self.restaurant_repository.get_with_menu(
            restaurant_id,
            city_id,
            self.user,
        )
        if restaurant:
            return RestaurantWithMenuDTO(**restaurant)
        return None

    async def restaurant_exists(self, restaurant_id: int) -> bool:
        return await self.restaurant_repository.get(restaurant_id) is not None

    @required_user
    async def restaurant_already_favorite(self, restaurant_id: int) -> bool:
        return await self.restaurant_repository.favorite_exists(
            self.user, restaurant_id
        )

    @required_user
    async def add_favorite_restaurant(self, restaurant_id: int) -> None:
        model_ = await self.restaurant_repository.add_favorite_restaurant(
            self.user, restaurant_id
        )
        await self.session.commit()
        await self.session.refresh(model_)
        return model_

    @required_user
    async def delete_favorite_restaurant(self, restaurant_id: int) -> None:
        await self.restaurant_repository.delete_favorite_restaurant(
            self.user, restaurant_id
        )
        await self.session.commit()

    async def dishes_exists(self, dishes: list[int], restaurant_id: int) -> bool:
        return await self.restaurant_repository.dishes_exists(dishes, restaurant_id)


InjectRestaurantService: TypeAlias = Annotated[RestaurantService, Depends()]
