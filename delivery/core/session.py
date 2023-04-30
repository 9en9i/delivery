from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from delivery.settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = async_sessionmaker(engine)
