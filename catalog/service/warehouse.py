from uuid import UUID
from fastapi import Depends
from models.db.catalog import Warehouse
from models.requests.warehouse import WarehouseReq

from repository.warehouse import WarehouseRepository


class WarehouseService:
    """Facade between db and request for shoes warehouse"""

    def __init__(self, repo: WarehouseRepository = Depends()) -> None:
        self.__repo = repo

    async def set_storage(self, model_id: UUID, payload: WarehouseReq) -> Warehouse:
        """Set storage manually. For admin usage only.

        Args:
            model_id (UUID): model identifier
            payload (WarehouseReq): request

        Returns:
            Warehouse: Warehouse for model
        """
        if payload.quantity <= 0:
            raise ValueError(
                "quantity",
                f"Quantity should be greater than 0. Requested {payload.quantity}",
            )
        return await self.__repo.set_storage(model_id, payload.size, payload.quantity)

    async def change_storage(self, model_id: UUID, payload: WarehouseReq):
        """Change number of pairs for model's size in warehouse

        Args:
            model_id (UUID): model_identifier
            payload (WarehouseReq): request
        """
        await self.__repo.change_storage(model_id, payload.size, payload.quantity)

    async def get_warehouse(self, model_id: UUID) -> Warehouse:
        """Get warehouse for model

        Args:
            model_id (UUID): model identifier

        Returns:
            Warehouse: Warehouse instance
        """
        return await self.__repo.get_warehouse(model_id)
