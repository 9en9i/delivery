from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    COOKING = "cooking"
    DELIVERED = "delivered"
    COMPLETED = "completed"
