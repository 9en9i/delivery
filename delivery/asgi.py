import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delivery.auth.views import router as auth_router
from delivery.cities.views import router as city_router
from delivery.orders.views import router as order_router
from delivery.restaurants.views.category import router as category_router
from delivery.restaurants.views.dish import router as dish_router
from delivery.restaurants.views.restaurant import router as restaurant_router
from delivery.users.views import router as user_router


app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(restaurant_router, prefix="/api")
app.include_router(city_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(dish_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(order_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serve():
    uvicorn.run("asgi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    serve()
