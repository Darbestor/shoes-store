from enum import Enum


class QueueName(str, Enum):
    ORDERS = "orders"
    CART = "cart"
    ORDER_HISTORY = "order_history"


class CartType(str, Enum):
    UPDATE = "cart.update"


class OrderHistoryType(str, Enum):
    ADD = "order_history.add"
