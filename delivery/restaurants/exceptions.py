from fastapi import HTTPException
from starlette import status


class RestaurantDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant does not exist",
        )


class RestaurantNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )


class DishesDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dishes does not exist",
        )


class RestaurantCantFavoriteRestaurant(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant can't favorite restaurant",
        )


class RestaurantCantUnavoriteRestaurant(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant can't unfavorite restaurant",
        )


class RestaurantAlreadyFavorite(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant already favorite",
        )


class RestaurantNotFavorite(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant not favorite",
        )
