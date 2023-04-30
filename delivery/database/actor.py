from sqlalchemy.orm import Mapped, mapped_column

from delivery.core.models.base import SQLModel
from delivery.core.security import create_password, verify_password


class ActorModel(SQLModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    salt: Mapped[str]

    def set_password(self, password: str):
        self.salt, self.hashed_password = create_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(
            salt=self.salt,
            password=password,
            hashed_password=self.hashed_password,
        )
