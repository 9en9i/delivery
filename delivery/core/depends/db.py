from typing import AsyncGenerator, Annotated

from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.session import SessionLocal
from delivery.settings import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


def get_storage() -> AsyncGenerator[Minio, None]:
    minio_client = Minio(
        settings.MINIO_HOSTNAME,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,
    )
    yield minio_client


InjectSession = Annotated[AsyncSession, Depends(get_db)]
InjectStorage = Annotated[Minio, Depends(get_storage)]
