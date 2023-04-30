from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.cities.controller import CityRepository
from delivery.core.depends.db import get_db
from delivery.database import CityModel


class CityService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db)],
        city_repository: Annotated[CityRepository, Depends()],
    ):
        self.session = session
        self.city_repository = city_repository

    async def get_all_cities(self) -> list[CityModel]:
        return (await self.session.scalars(self.city_repository.get_all_query())).all()


InjectCityService: TypeAlias = Annotated[CityService, Depends()]
