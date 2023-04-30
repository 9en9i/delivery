from abc import abstractmethod, ABC
from typing import Generic, TypeVar

from sqlalchemy import select

from delivery.core.controllers.base import BaseController
from delivery.database.actor import ActorModel

T = TypeVar("T", bound=ActorModel)


class ActorController(BaseController, ABC, Generic[T]):
    model = ActorModel

    async def get_by_email(self, email: str) -> T | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def auth(self, email: str, password: str) -> T | None:
        user = await self.get_by_email(email)
        if user and user.check_password(password):
            return user

    async def exists(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None

    @abstractmethod
    async def create(self, **kwargs) -> T:
        password = kwargs.pop("password")
        model_ = self.model(**kwargs)
        model_.set_password(password)
        return model_

    #
    # async def create(self, email: str, password: str) -> UserModel:
    #     user = UserModel(email=email, role=role)
    #     user.set_password(password)
    #     self.session.add(user)
    #     await self.session.commit()
    #     await self.session.refresh(user)
    #     return user
