from typing import Annotated, TypeAlias

from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from delivery.core.depends.db import InjectSession
from delivery.core.enums.actors import ActorEnum
from delivery.database import UserModel, RestaurantModel
from delivery.settings import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token",
    scopes={
        "user": "User",
        "restaurant": "Restaurant",
    },
    auto_error=False,
)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def _require_actor(
    token: str,
    actor_type: ActorEnum | None,
) -> tuple[str, ActorEnum]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        user_type: str = payload.get("type")
        if email is None or user_type is None:
            raise credentials_exception
        decoded_actor_type = ActorEnum(user_type)
        if actor_type is None:
            return email, decoded_actor_type
        if decoded_actor_type != actor_type:
            raise credentials_exception
    except (JWTError, ValueError, AttributeError):
        raise credentials_exception
    return email, decoded_actor_type


def require_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> tuple[str, ActorEnum]:
    return _require_actor(token, ActorEnum.USER)


def require_restaurant(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> tuple[str, ActorEnum]:
    return _require_actor(token, ActorEnum.RESTAURANT)


def require_actor(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> tuple[str, ActorEnum]:
    user = _require_actor(token, None)
    return user


def not_require_actor(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> tuple[str, ActorEnum] | None:
    try:
        user = _require_actor(token, None)
        return user
    except HTTPException:
        return None


InjectUser: TypeAlias = Annotated[tuple[str, ActorEnum], Depends(require_user)]
InjectRestaurant: TypeAlias = Annotated[
    tuple[str, ActorEnum], Depends(require_restaurant)
]
InjectActor: TypeAlias = Annotated[tuple[str, ActorEnum], Depends(require_actor)]
InjectMaybeActor: TypeAlias = Annotated[
    tuple[str, ActorEnum] | None, Depends(not_require_actor)
]


async def maybe_user(
    user: InjectMaybeActor, session: InjectSession
) -> UserModel | RestaurantModel | None:
    if user is None:
        return None
    actor_type = user[1]
    actor_email = user[0]
    if actor_type == ActorEnum.RESTAURANT:
        restaurant = await session.scalar(
            select(RestaurantModel).where(RestaurantModel.email == actor_email)
        )
        if restaurant is None:
            raise credentials_exception
        return restaurant
    else:
        user_actor = await session.scalar(
            select(UserModel).where(UserModel.email == actor_email)
        )
        if user_actor is None:
            raise credentials_exception
        return user_actor


InjectMaybeUser: TypeAlias = Annotated[
    UserModel | RestaurantModel | None, Depends(maybe_user)
]
