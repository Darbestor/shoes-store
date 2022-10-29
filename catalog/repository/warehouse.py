"""Warehouse repository for shoes"""

from uuid import UUID
from exceptions import DBException
from models.db.catalog import Storage, Warehouse


class WarehouseRepository:
    """Repository"""

    async def update_storage(
        self, model_id: UUID, size: int, quantity: int
    ) -> Warehouse:
        """Update warehouse for shoes

        Args:
            model_id (UUID): model identifier
            size (int): shoes size
            quantity (int): number of pairs

        Returns:
            Warehouse: updated warehouse for model
        """
        warehouse = await Warehouse.find(Warehouse.model_id == model_id).first_or_none()
        if warehouse is None:
            raise DBException(f"Storage for {model_id} not found")
        storage = next((s for s in warehouse.storage if s.size == size), None)
        if storage is None:
            storage = Storage(size=size, quantity=quantity)
            warehouse.storage.append(storage)
        else:
            storage.quantity = quantity
        await warehouse.save()
        return warehouse
