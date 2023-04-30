from abc import ABC
from typing import Type

from sqlalchemy import select

from delivery.core.depends.db import InjectSession
from delivery.core.models.base import SQLModel


class BaseController(ABC):
    model: Type[SQLModel] = None

    def __init__(self, db: InjectSession):
        self.session = db

    async def get(self, model_id: int) -> model:
        return await self.session.get(self.model, model_id)

    def get_all_query(self, limit: int | None = None, offset: int | None = None):
        query = select(self.model)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query

    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ):
        return (await self.get_all_query(limit, offset)).all()

    async def exists(self, model_id: int) -> bool:
        return await self.get(model_id) is not None
