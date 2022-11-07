import json
from rabbitmq.message_handlers.base import HandlerBase
from rabbitmq.models import OrderCreate
from repository.order import OrderRepository
from service.order import OrderService


class Create(HandlerBase):
    async def handle(self):
        await super().handle()
        service = OrderService(repo=OrderRepository())
        model_dict = json.loads(self._message.body)

        items = {item["item_id"]: item["quantity"] for item in model_dict["items"]}
        payload = OrderCreate(user_id=model_dict["id"], items=items)
        await service.create_order(payload)
        await self._message.ack()
