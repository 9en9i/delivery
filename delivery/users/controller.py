from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.controllers.actor import ActorController
from delivery.core.depends.db import get_db
from delivery.database import UserModel


class UserRepository(ActorController[UserModel]):
    model = UserModel

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        super().__init__(db)

    async def create(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        city_id: int,
    ) -> UserModel:
        return await super().create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            city_id=city_id,
        )
