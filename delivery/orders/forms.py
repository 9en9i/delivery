from pydantic import BaseModel


class OrderDishForm(BaseModel):
    dish_id: int
    amount: int


class OrderForm(BaseModel):
    restaurant_id: int
    address: str
    dishes: list[OrderDishForm]

    @property
    def dish_ids(self) -> list[int]:
        return [i.dish_id for i in self.dishes]
