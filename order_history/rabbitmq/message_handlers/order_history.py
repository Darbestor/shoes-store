import json
from models.db.models import Order
from models.requests.order_history import OrderReq
from rabbitmq.message_handlers.base import HandlerBase
from repository.order_history import OrderHistoryRepository
from service.order import OrderHistoryService


class Add(HandlerBase):
    async def handle(self):
        await super().handle()
        service = OrderHistoryService(repo=OrderHistoryRepository())
        model_dict = json.loads(self._message.body)

        model_dict["created_date"] = self._message.timestamp
        order = Order(**model_dict)
        payload = OrderReq(user_id=model_dict["user_id"], order=order)
        await service.add_order(payload)
        await self._message.ack()
