from typing import cast, Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.controllers.base import BaseController
from delivery.core.depends.db import get_db
from delivery.database import CityModel


class CityRepository(BaseController):
    model = CityModel

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        super().__init__(db)

    async def get_by_ids(self, cities: set[int]) -> model:
        return cast(
            self.model,
            (
                await self.session.scalars(
                    select(self.model).where(self.model.id.in_(cities))
                )
            ).all(),
        )


InjectCityRepository: TypeAlias = Annotated[CityRepository, Depends()]
