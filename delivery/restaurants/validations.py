from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.depends.auth import InjectMaybeUser
from delivery.core.depends.db import get_db
from delivery.database import UserModel, RestaurantModel


class RestaurantValidations:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db)],
        user: InjectMaybeUser,
    ):
        self.session = session
        self.user = user

    async def is_restaurant(self) -> bool:
        return isinstance(self.user, RestaurantModel)

    async def validate(self, condition, error):
        if await condition:
            raise error


InjectRestaurantValidations: TypeAlias = Annotated[RestaurantValidations, Depends()]
