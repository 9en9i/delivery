import datetime
from collections.abc import Sequence
from typing import Annotated, TypeAlias

from fastapi import Depends, UploadFile
from minio import Minio
from sqlalchemy import select, delete, func, RowMapping, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from delivery.core.controllers.actor import ActorController
from delivery.core.depends.db import get_db, get_storage
from delivery.database import CityModel, RestaurantCityAssociation, UserModel
from delivery.database.restaurant import (
    RestaurantModel,
    RestaurantCategoryModel,
    DishModel,
    FavoriteRestaurant,
)


class RestaurantRepository(ActorController[RestaurantModel]):
    model = RestaurantModel

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db)],
        storage: Annotated[Minio, Depends(get_storage)],
    ):
        super().__init__(session)
        self.storage = storage

    async def get_all(
        self,
        city_id: int,
        user: UserModel | None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[RowMapping]:
        stmt = (
            select(
                RestaurantModel.id,
                RestaurantModel.name,
                RestaurantModel.description,
                RestaurantModel.image,
                RestaurantCityAssociation.opening_time,
                RestaurantCityAssociation.closing_time,
                FavoriteRestaurant.user_id.isnot(None).label("is_favorite")
                if user and isinstance(user, UserModel)
                else literal_column("NULL").label("is_favorite"),
            )
            .join(
                RestaurantCityAssociation,
                RestaurantModel.id == RestaurantCityAssociation.restaurant_id,
            )
            .where(RestaurantCityAssociation.city_id == city_id)
        )
        if user:
            stmt = stmt.outerjoin(
                FavoriteRestaurant,
                (RestaurantModel.id == FavoriteRestaurant.restaurant_id)
                & (FavoriteRestaurant.user_id == user.id),
            )
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        restaurants = (await self.session.execute(stmt)).mappings().all()
        return restaurants

    async def create(
        self,
        name: str,
        description: str,
        email: str,
        password: str,
        cities: set[int],
    ) -> model:
        return await super().create(
            name=name,
            email=email,
            password=password,
            description=description,
        )

    async def add_image(self, restaurant_id: int, image: UploadFile) -> model:
        restaurant = await self.get(restaurant_id)
        restaurant.image = await self.storage.put_object(
            "images",
            image.filename,
            image.file,
            image.content_type,
        )
        return await self.update(restaurant)

    async def get_restaurant_with_menu(self, restaurant_id: int):
        return await self.session.scalars(
            select(self.model)
            .where(self.model.id == restaurant_id)
            .options(
                joinedload(self.model.categories),
                joinedload(self.model.dishes),
            )
        )

    async def add_cities(
        self,
        restaurant_id: int,
        cities: list[CityModel],
        open_time: datetime.time,
        close_time: datetime.time,
    ) -> None:
        for i in cities:
            self.session.add(
                RestaurantCityAssociation(
                    restaurant_id=restaurant_id,
                    city_id=i.id,
                    opening_time=open_time,
                    closing_time=close_time,
                )
            )

    async def category_exists(self, user: RestaurantModel, name: str) -> bool:
        return (
            await self.session.scalar(
                select(self.model)
                .join(
                    RestaurantCategoryModel,
                    self.model.id == RestaurantCategoryModel.restaurant_id,
                )
                .where(
                    RestaurantCategoryModel.name == name,
                    self.model.id == user.id,
                )
            )
            is not None
        )

    async def category_exists_by_id(
        self,
        user: RestaurantModel,
        category_id: int,
    ) -> bool:
        return (
            await self.session.scalar(
                select(self.model)
                .join(
                    RestaurantCategoryModel,
                    self.model.id == RestaurantCategoryModel.restaurant_id,
                )
                .where(
                    RestaurantCategoryModel.id == category_id,
                    self.model.id == user.id,
                )
            )
            is not None
        )

    async def add_category(
        self, user: RestaurantModel, name: str
    ) -> RestaurantCategoryModel:
        model_ = RestaurantCategoryModel(
            restaurant_id=user.id,
            name=name,
        )
        self.session.add(model_)
        return model_

    async def delete_category(self, user: RestaurantModel, category_id: int) -> None:
        await self.session.execute(
            delete(RestaurantCategoryModel).where(
                RestaurantCategoryModel.restaurant_id == user.id,
                RestaurantCategoryModel.id == category_id,
            )
        )

    async def get_with_menu(
        self,
        restaurant_id: int,
        city_id: int,
        user: UserModel | None,
    ):
        r = aliased(RestaurantModel)
        rc = aliased(RestaurantCityAssociation)
        rf = aliased(FavoriteRestaurant)
        c = aliased(CityModel)
        rcat = aliased(RestaurantCategoryModel)
        d = aliased(DishModel)

        dish_query = (
            select(func.json_agg(literal_column("dish")))
            .select_from(
                select(d.id, d.name, d.price, d.description, d.image)
                .where(d.category_id == rcat.id)
                .correlate(rcat)
                .alias("dish")
            )
            .scalar_subquery()
        )

        categories_query = (
            select(func.json_agg(literal_column("category")))
            .select_from(
                select(rcat.id, rcat.name, dish_query.label("dishes"))
                .select_from(rcat)
                .correlate(r)
                .where(rcat.restaurant_id == r.id)
                .alias("category")
            )
            .scalar_subquery()
        )

        query = (
            select(
                r.id,
                r.name,
                r.description,
                r.image,
                rc.opening_time,
                rc.closing_time,
                categories_query.label("categories"),
                rf.user_id.isnot(None).label("is_favorite")
                if user and isinstance(user, UserModel)
                else literal_column("NULL").label("is_favorite"),
            )
            .join(rc, r.id == rc.restaurant_id)
            .join(c, c.id == rc.city_id)
            .where((rc.city_id == city_id) & (r.id == restaurant_id))
            .group_by(
                r.id,
                r.name,
                r.description,
                r.image,
                rc.opening_time,
                rc.closing_time,
            )
        )
        if user:
            query = query.outerjoin(
                rf,
                (r.id == rf.restaurant_id) & (rf.user_id == user.id),
            ).group_by(literal_column("is_favorite"))
        r = (await self.session.execute(query)).mappings().first()
        return r

    async def create_dish(
        self,
        user: RestaurantModel,
        category_id: int,
        name: str,
        description: str,
        price: float,
    ) -> DishModel:
        dish = DishModel(
            restaurant_id=user.id,
            category_id=category_id,
            name=name,
            description=description,
            price=price,
        )
        self.session.add(dish)
        return dish

    async def dish_exists(self, user: RestaurantModel, dish_id: int) -> bool:
        return (
            await self.session.scalar(
                select(DishModel)
                .join(
                    RestaurantModel,
                    RestaurantModel.id == DishModel.restaurant_id,
                )
                .where(
                    DishModel.id == dish_id,
                    RestaurantModel.id == user.id,
                )
            )
            is not None
        )

    async def delete_dish(self, dish_id: int) -> None:
        await self.session.execute(delete(DishModel).where(DishModel.id == dish_id))

    async def get_dish_by_id(self, user: RestaurantModel, dish_id: int) -> DishModel:
        return await self.session.scalar(
            select(DishModel)
            .join(RestaurantModel)
            .where(
                DishModel.id == dish_id,
                DishModel.restaurant_id == user.id,
            )
        )

    async def add_favorite_restaurant(
        self, user: UserModel, restaurant_id: int
    ) -> FavoriteRestaurant:
        model_ = FavoriteRestaurant(
            user_id=user.id,
            restaurant_id=restaurant_id,
        )
        self.session.add(model_)
        return model_

    async def delete_favorite_restaurant(
        self, user: UserModel, restaurant_id: int
    ) -> None:
        await self.session.execute(
            delete(FavoriteRestaurant).where(
                FavoriteRestaurant.user_id == user.id,
                FavoriteRestaurant.restaurant_id == restaurant_id,
            )
        )

    async def favorite_exists(self, user: UserModel, restaurant_id: int) -> bool:
        return (
            await self.session.scalar(
                select(FavoriteRestaurant).where(
                    FavoriteRestaurant.user_id == user.id,
                    FavoriteRestaurant.restaurant_id == restaurant_id,
                )
            )
            is not None
        )

    async def dishes_exists(self, dishes: list[int], restaurant_id: int) -> bool:
        return len(
            (
                await self.session.scalars(
                    select(DishModel).where(
                        DishModel.id.in_(dishes),
                        DishModel.restaurant_id == restaurant_id,
                    )
                )
            ).all()
        ) == len(dishes)

    async def dish_already_exists(self, user: RestaurantModel, name: str):
        return (
            await self.session.scalar(
                select(DishModel)
                .join(RestaurantModel)
                .where(
                    DishModel.name == name,
                    DishModel.restaurant_id == user.id,
                )
            )
            is not None
        )


InjectRestaurantRepository: TypeAlias = Annotated[RestaurantRepository, Depends()]
