"""Warehouse repository for shoes"""

from uuid import UUID
from exceptions import DBException
from models.db.catalog import Storage, Warehouse


class WarehouseRepository:
    """Repository"""

    async def set_storage(self, model_id: UUID, size: int, quantity: int) -> Warehouse:
        """Update warehouse for shoes

        Args:
            model_id (UUID): model identifier
            size (int): shoes size
            quantity (int): number of pairs

        Returns:
            Warehouse: updated warehouse for model
        """
        warehouse = await self.get_warehouse(model_id)
        if warehouse is None:
            raise DBException(f"Storage for model {model_id} not found")
        storage = next((s for s in warehouse.storage if s.size == size), None)
        if storage is None:
            storage = Storage(size=size, quantity=quantity)
            warehouse.storage.append(storage)
        else:
            storage.quantity = quantity
        await warehouse.save()
        return warehouse

    async def change_storage(self, model_id: UUID, size: int, quantity: int):
        """Return pairs back to storage

        Args:
            model_id (UUID): model_identifier
            size (int): model size
            quantity (int): number of pairs.
                Positive number - return models to storage
                Negative number - take models from storage.

            Raises:
            DBException:
                Storage not found
            ValueException:
                Number of pairs in storage is less than quantity to take.
                Size is not found
        """
        warehouse = await self.get_warehouse(model_id)
        if warehouse is None:
            raise DBException(f"Storage for model {model_id} not found")
        storage = next((s for s in warehouse.storage if s.size == size), None)
        if storage is None:
            raise ValueError("size", f"Size for model {model_id} not found")
        storage.quantity += quantity
        if storage.quantity < 0:
            raise ValueError(
                "quantity", f"Not enough pairs in warehouse for model {model_id}"
            )
        await warehouse.save()

    async def get_warehouse(self, model_id: UUID):
        return await Warehouse.find(Warehouse.model_id == model_id).first_or_none()
