from typing import Annotated, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.auth.service import ActorService
from delivery.cities.controller import CityRepository
from delivery.core.depends.db import get_db
from delivery.core.enums.actors import ActorEnum
from delivery.database import UserModel
from delivery.users.controller import UserRepository

T = TypeVar("T")


class UserService(ActorService):
    repository: UserRepository
    actor_type = ActorEnum.USER

    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends()],
        city_repository: Annotated[CityRepository, Depends()],
        session: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.user_repository = user_repository
        self.city_repository = city_repository
        self.session = session

    async def auth(self, email: str, password: str) -> UserModel | None:
        return await self.user_repository.get_by_email(email)

    async def email_not_exists(self, email: str) -> bool:
        return await self.user_repository.exists(email)

    async def invalid_city(self, city_id: int) -> bool:
        return not await self.city_repository.exists(city_id)

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        city_id: int,
    ) -> UserModel:
        model_ = await self.user_repository.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            city_id=city_id,
        )
        self.session.add(model_)
        await self.session.commit()
        await self.session.refresh(model_)
        return model_
