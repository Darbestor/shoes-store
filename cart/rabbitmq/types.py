from enum import Enum


class QueueName(str, Enum):
    ORDERS = "orders"
    CART = "cart"


class CartType(str, Enum):
    UPDATE = "cart.update"


class OrderType(str, Enum):
    CREATE = "orders.create"
