from uuid import UUID
from fastapi import Depends
from models.requests.warehouse import WarehouseReq

from repository.warehouse import WarehouseRepository


class WarehouseService:
    """Facade between db and request for shoes warehouse"""

    def __init__(self, repo: WarehouseRepository = Depends()) -> None:
        self.repo = repo

    async def update_storage(self, model_id: UUID, payload: WarehouseReq):
        await self.repo.update_storage(model_id, payload.size, payload.quantity)
