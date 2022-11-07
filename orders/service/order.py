from uuid import UUID
from fastapi import Depends
from models.db.models import Order
from models.requests.order import OrderInfoReq
from rabbitmq.client import RabbitMQClient, RabbitMQClientFactory
from rabbitmq.models import OrderCreate
from rabbitmq.types import CartType, OrderHistoryType, QueueName
from repository.order import OrderRepository


class OrderService:
    def __init__(
        self,
        repo: OrderRepository = Depends(),
        rabbitmq_cart_client: RabbitMQClient = Depends(
            lambda: RabbitMQClientFactory.get_client(QueueName.CART.value)
        ),
        rabbitmq_history_client: RabbitMQClient = Depends(
            lambda: RabbitMQClientFactory.get_client(QueueName.ORDER_HISTORY.value)
        ),
    ) -> None:
        self.__repo = repo
        self.__rabbitmq_cart_client = rabbitmq_cart_client
        self.__rabbitmq_history_client = rabbitmq_history_client

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
        order = await self._cancel_order(order_id)
        async with self.__rabbitmq_cart_client as client:
            await client.publish(CartType.UPDATE.value, order)

    async def confirm_order(self, info: OrderInfoReq):
        info_dict = info.dict(exclude_unset=True)
        order_id = info_dict.pop("order_id")
        order = await self.__repo.delete_order(order_id)

        # fill order information before sending to history
        for key, value in info_dict.items():
            setattr(order, key, value)
        async with self.__rabbitmq_history_client as client:
            await client.publish(OrderHistoryType.ADD.value, order)

    async def get_order(self, order_id: UUID) -> Order:
        return await self.__repo.get_order(order_id)

    async def get_user_orders(self, user_id: UUID) -> list[Order]:
        return await self.__repo.get_user_orders(user_id)

    async def _cancel_order(self, order_id: UUID):
        order = await self.__repo.delete_order(order_id)
        # TODO return items from order to stock
        return order
