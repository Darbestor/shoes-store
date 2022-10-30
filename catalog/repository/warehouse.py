"""Warehouse repository for shoes"""

from typing import Tuple
from uuid import UUID
from exceptions import DBException, ValueException
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
        warehouse = await self.get_warehouse(model_id)
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

    async def return_pairs(self, model_id: UUID, size: int, quantity):
        """Return pairs back to storage

        Args:
            model_id (UUID): model_identifier
            size (int): model size
            quantity (_type_): number of pairs to return

        """
        warehouse, storage = await self.__get_storage(model_id, size)
        storage.quantity += quantity
        await warehouse.save()

    async def take_pairs(self, model_id: UUID, size: int, quantity):
        """Take models from warehouse

        Args:
            model_id (UUID): model_identifier
            size (int): model size
            quantity (_type_): number of pairs to take

        """
        warehouse, storage = await self.__get_storage(model_id, size)
        if quantity > storage.quantity:
            raise ValueException(f"Not enough pairs in warehouse for {model_id}")

        storage.quantity -= quantity
        await warehouse.save()

    async def __get_storage(self, model_id, size) -> Tuple[Warehouse, Storage]:
        """Get size storage for model

        Args:
            model_id (_type_): model identifier
            size (_type_): model size

        Returns:
            Tuple[Warehouse, Storage]: Model's Warehouse and size storage
        """
        warehouse = await self.get_warehouse(model_id)
        if warehouse is None:
            raise DBException(f"Storage for {model_id} not found")
        storage = next((s for s in warehouse.storage if s.size == size), None)
        if storage is None:
            raise ValueException(f"Size for {model_id} not found")
        return warehouse, storage

    async def get_warehouse(self, model_id: UUID):
        return await Warehouse.find(Warehouse.model_id == model_id).first_or_none()
