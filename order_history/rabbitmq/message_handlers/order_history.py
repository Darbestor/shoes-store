import json
from models.requests.order_history import OrderReq
from rabbitmq.message_handlers.base import HandlerBase
from repository.order_history import OrderHistoryRepository
from service.order import OrderHistoryService


class Add(HandlerBase):
    async def handle(self):
        await super().handle()
        service = OrderHistoryService(repo=OrderHistoryRepository())
        model_dict = json.loads(self._message.body)

        payload = OrderReq(user_id=model_dict["id"], items=model_dict)
        await service.add_order(payload)
        await self._message.ack()
