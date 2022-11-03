from uuid import UUID
from fastapi import Depends
from models.db.models import Order
from models.requests.order import OrderInfoReq
from rabbitmq.models import OrderCreate
from repository.order import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository = Depends()) -> None:
        self.__repo = repo

    async def create_order(self, payload: OrderCreate) -> Order:
        """Create order

        Args:
            payload (OrderCreate): message body from rabbitmq

        Returns:
            Order: Instance of Order
        """
        # TODO reserve items for order
        return await self.__repo.add_order(payload.user_id, payload.items)

    async def delete_order(self, order_id: UUID):
        await self._cancel_order(order_id)

    async def change_order(self, order_id: UUID):
        await self._cancel_order(order_id)
        # TODO send order back to cart

    async def confirm_order(self, order_id: UUID):
        order = await self.__repo.get_order(order_id)
        # send order to order history

    async def update_order_info(self, payload: OrderInfoReq) -> Order:
        info_dict = payload.dict(exclude_unset=True)
        order_id = info_dict.pop("order_id")
        return await self.__repo.update_order(order_id, info_dict)

    async def get_order(self, order_id: UUID) -> Order:
        return await self.__repo.get_order(order_id)

    async def get_user_orders(self, user_id: UUID) -> list[Order]:
        return await self.__repo.get_user_orders(user_id)

    async def _cancel_order(self, order_id: UUID):
        order = await self.__repo.delete_order(order_id)
        # TODO return items from order to stock
        return order
