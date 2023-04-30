from delivery.core.schema import BaseSchema


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class UserSchema(BaseSchema):
    id: int
    email: str
    first_name: str
    last_name: str
