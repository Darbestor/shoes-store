from enum import Enum


class OrdersType(str, Enum):
    CREATE = "orders.create"


class CartType(str, Enum):
    UPDATE = "cart.update"
