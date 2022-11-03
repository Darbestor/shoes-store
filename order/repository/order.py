"""Manipulation of Order documents in database"""

from datetime import datetime
from uuid import UUID

from models.db.models import Order, Item


class OrderRepository:
    """Repository"""

    async def add_order(self, user_id: UUID, items: dict[UUID, int]) -> Order:
        """Add user order.
        Args:
            user_id (UUID): user identifier
            item_id (dict[UUID, int]): items list.
                UUID - item_id
                int - quantity

        Returns:
            Order: created order
        """

        order_items = [
            Item(item_id=item_id, quantity=quant) for item_id, quant in items.items()
        ]
        order = Order(
            user_id=user_id,
            items=order_items,
            address=None,
            shipping_date=None,
            phone=None,
            total_price=0,
            created_date=datetime.utcnow(),
        )

        await order.save()
        return order

    async def update_order(self, order_id: UUID, details: dict) -> Order:
        """Update order information

        Args:
            order_id (UUID): Order identifier
            details (dict): details

        Returns:
            Order: Updated order instance
        """
        order = await self.get_order(order_id)
        for key, value in details.items():
            setattr(order, key, value)
        await order.save()

        return order

    async def delete_order(self, order_id: UUID) -> Order:
        """Delete order

        Args:
            order_id (UUID): order identifier

        Returns:
            Order: deleted order info
        """
        order = await self.get_order(order_id)
        await order.delete()
        return order

    async def get_order(self, order_id: UUID) -> Order:
        order = await Order.find_one(Order.id == order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found")
        return order

    async def get_user_orders(self, user_id) -> list[Order]:
        return await Order.find(Order.user_id == user_id).to_list()
