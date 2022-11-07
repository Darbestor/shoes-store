import json
from rabbitmq.message_handlers.base import HandlerBase
from repository.bin import BinRepository
from service.cart import BinService


class Update(HandlerBase):
    async def handle(self):
        await super().handle()
        service = BinService(repo=BinRepository())
        model_dict = json.loads(self._message.body)

        items = {item["item_id"]: item["quantity"] for item in model_dict["items"]}
        await service.update_bin(model_dict["user_id"], items)
        await self._message.ack()
