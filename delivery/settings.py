from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class _Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    MINIO_HOSTNAME: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MEDIA_URL: str

    class Config:
        env_file = BASE_DIR.parent / ".env"
        env_prefix = "DELIVERY__"


settings = _Settings()
