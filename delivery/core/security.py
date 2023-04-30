from datetime import timedelta, datetime

import bcrypt
from jose import jwt
from passlib.context import CryptContext

from delivery.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _generate_salt() -> str:
    return bcrypt.gensalt().decode()


def _generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_password(password: str) -> (str, str):
    salt = _generate_salt()
    hashed_password = _generate_password_hash(salt + password)
    return salt, hashed_password


def verify_password(salt: str, password: str, hashed_password: str) -> bool:
    return pwd_context.verify(salt + password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
