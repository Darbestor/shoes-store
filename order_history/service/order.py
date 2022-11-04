from uuid import UUID
from fastapi import Depends
from models.db.models import Order, OrderHistory
from models.requests.order_history import OrderInfoReq
from rabbitmq.client import RabbitMQClient, RabbitMQClientFactory
from rabbitmq.models import OrderCreate
from rabbitmq.types import CartType, OrderHistoryType, QueueName
from repository.order_history import OrderHistoryRepository


class OrderHistoryService:
    def __init__(
        self,
        repo: OrderHistoryRepository = Depends(),
    ) -> None:
        self.__repo = repo

    async def add_order(self, payload: OrderReq) -> OrderHistory:
        """Add  user order to history

        Args:
            payload (OrderCreate): message body from rabbitmq

        Returns:
            OrderHistory: User's order history
        """

        return await self.__repo.add_order(payload.user_id, payload.order)

    async def delete_order(self, order_id: UUID):
        await self._cancel_order(order_id)

    async def change_order(self, order_id: UUID):
        order = await self._cancel_order(order_id)
        await self.__rabbitmq_cart_client.publish(CartType.UPDATE.value, order)

    async def confirm_order(self, info: OrderInfoReq):
        info_dict = info.dict(exclude_unset=True)
        order_id = info_dict.pop("order_id")
        order = await self.__repo.delete_order(order_id)

        # fill order information before sending to history
        for key, value in info_dict.items():
            setattr(order, key, value)
        await self.__rabbitmq_history_client.publish(OrderHistoryType.ADD.value, order)

    async def get_order(self, order_id: UUID) -> OrderHistory:
        return await self.__repo.get_order(order_id)

    async def get_user_orders(self, user_id: UUID) -> list[OrderHistory]:
        return await self.__repo.get_user_orders(user_id)

    async def _cancel_order(self, order_id: UUID):
        order = await self.__repo.delete_order(order_id)
        # TODO return items from order to stock
        return order
