from typing import Annotated

from pydantic import EmailStr
from pydantic.fields import Field

from delivery.core.schema import BaseSchema


class JoinUserForm(BaseSchema):
    email: EmailStr
    password: Annotated[str, Field(max_length=50, min_length=6)]
    first_name: Annotated[str, Field(max_length=50, min_length=2)]
    last_name: Annotated[str, Field(max_length=50, min_length=2)]
    city_id: Annotated[int, Field(gt=0)]
