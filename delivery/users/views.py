from typing import Annotated, cast

from fastapi import Depends, APIRouter, HTTPException, status

from delivery.core.validation import validate
from delivery.users.form import JoinUserForm
from delivery.users.schema import UserSchema
from delivery.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/join")
async def join(
    form: JoinUserForm,
    user_service: Annotated[UserService, Depends()],
) -> UserSchema:
    validate(
        await user_service.email_not_exists(form.email),
        HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Email already registered",
        ),
    )
    validate(
        await user_service.invalid_city(form.city_id),
        HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Invalid city",
        ),
    )
    return cast(
        UserSchema,
        await user_service.create_user(
            email=form.email,
            password=form.password,
            first_name=form.first_name,
            last_name=form.last_name,
            city_id=form.city_id,
        ),
    )
