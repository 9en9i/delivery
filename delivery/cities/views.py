from typing import cast

from fastapi import APIRouter

from delivery.cities.schemas import CitySchema
from delivery.cities.service import InjectCityService

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("")
async def read_all_cities(
    city_service: InjectCityService
) -> list[CitySchema]:
    return cast(list[CitySchema], await city_service.get_all_cities())
