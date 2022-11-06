"""Manipulation of Order history documents in database"""

from uuid import UUID
from models.db.models import Order, OrderHistory


class OrderHistoryRepository:
    """Repository"""

    async def add_order(self, user_id: UUID, order: Order) -> OrderHistory:
        """Add order to history.
        Args:
            user_id (UUID): user identifier
            order (OrderReq): payload

        Returns:
            OrderHistory: updated instance for user's order history
        """

        history = await OrderHistory.find_one(OrderHistory.id == user_id)
        if history is None:
            history = OrderHistory(id=user_id, orders=[])

        history.orders.append(order)
        await history.save()
        return history

    async def get_history(self, user_id: UUID) -> OrderHistory:
        order = await OrderHistory.find_one(OrderHistory.id == user_id)
        if order is None:
            raise ValueError(f"Order history for '{user_id}' not found")
        return order
