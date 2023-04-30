from fastapi import HTTPException
from starlette import status


class InvalidCities(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cities",
        )
