from asyncio import iscoroutinefunction
from functools import wraps

from fastapi import HTTPException, status


def required_user(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        if iscoroutinefunction(func):
            return await func(self, *args, **kwargs)
        return func(self, *args, **kwargs)

    return wrapper
