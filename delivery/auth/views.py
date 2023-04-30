from datetime import timedelta
from typing import Annotated, cast

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from delivery.auth.schema import TokenSchema
from delivery.auth.service import ActorService
from delivery.core.enums.actors import ActorEnum
from delivery.core.security import create_access_token
from delivery.core.validation import validate
from delivery.restaurants.service import RestaurantService
from delivery.settings import settings
from delivery.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


INCORRECT_EMAIL_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

INCORRECT_SCOPE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect scope",
)


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    actor_service: Annotated[ActorService, Depends()],
    user_service: Annotated[UserService, Depends()],
    restaurant_service: Annotated[RestaurantService, Depends()],
) -> TokenSchema:
    validate(
        actor_service.Validation.to_many_scopes(form_data.scopes),
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many scopes",
        ),
    )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if form_data.scopes == [ActorEnum.USER]:
        user = await user_service.auth(form_data.username, form_data.password)
        validate(
            not user,
            INCORRECT_EMAIL_OR_PASSWORD,
        )
        access_token = create_access_token(
            data={
                "sub": user.email,
                "type": "user",
            },
            expires_delta=access_token_expires,
        )
    elif form_data.scopes == [ActorEnum.RESTAURANT]:
        restaurant = await restaurant_service.auth(
            form_data.username, form_data.password
        )
        validate(
            not restaurant,
            INCORRECT_EMAIL_OR_PASSWORD,
        )
        access_token = create_access_token(
            data={
                "sub": restaurant.email,
                "type": "restaurant",
            },
            expires_delta=access_token_expires,
        )
    else:
        raise INCORRECT_SCOPE
    return cast(TokenSchema, {"access_token": access_token, "token_type": "bearer"})
