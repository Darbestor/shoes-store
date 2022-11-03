"""Manipulation of Bin documents in database"""

from uuid import UUID
from exceptions import DBException

from models.db.models import Bin, Item


class BinRepository:
    """Repository"""

    async def add_item(self, user_id: UUID, item_id: UUID, quantity: int) -> Bin:
        """Add item to cart.
        If cart does not exist, create one and add item to it

        Args:
            user_id (UUID): user identifier
            item_id (UUID): item identifier
            quantity (int): quantity

        Raises:
            DBException: Database exception

        Returns:
            Bin: updated bin
        """
        if quantity < 1:
            raise ValueError("quantity", "Quantity must be greater than 0")

        bin_ = await Bin.find(Bin.id == user_id).first_or_none()

        if bin_ is None:
            items = [Item(item_id=item_id, quantity=quantity)]
            bin_ = Bin(id=user_id, items=items)
        else:
            item = next((x for x in bin_.items if x.item_id == item_id), None)
            if item is not None:
                item.quantity += quantity
            else:
                bin_.items.append(Item(item_id=item_id, quantity=quantity))

        await bin_.save()
        return bin_

    async def remove_item(self, user_id: UUID, item_id: UUID, quantity: int) -> Bin:
        """Remove item from bin if item's quantity is equal to or grater than quantity.
        Otherwise decrease quantity

        Args:
            user_id (UUID): user identifier
            item_id (UUID): item identifier
            quantity (int): quantity to remove

        Raises:
            ValueError: item not found

        Returns:
            Bin: updated Bin instance
        """
        bin_ = await self.get_bin(user_id)
        item = next((x for x in bin_.items if x.item_id == item_id), None)
        if item is None:
            raise ValueError("item_id", "item not found")
        if quantity >= item.quantity:
            bin_.items.remove(item)
        else:
            item.quantity -= quantity
        await bin_.save()
        return bin_

    async def update_bin(self, user_id: UUID, items: dict[UUID, int]):
        """Update items in bin in case user want to change an order

        Args:
            user_id (UUID): user identifier
        """
        bin_ = await Bin.find(Bin.id == user_id).first_or_none()

        if bin_ is None:
            bin_ = Bin(id=user_id)
        bin_.items = [
            Item(item_id=id_, quantity=quantity) for id_, quantity in items.items()
        ]
        await bin_.save()

    async def remove_bin(self, user_id: UUID) -> Bin:
        """Clear bin for user

        Args:
            user_id (UUID): user identifier

        Returns:
            Bin: Removed bin information
        """
        bin_ = await self.get_bin(user_id)
        await bin_.delete()
        return bin_

    async def get_bin(self, user_id: UUID) -> Bin:
        """Get users bin

        Args:
            user_id (UUID): user identifier

        Raises:
            DBException: Cart not found

        Returns:
            Bin: Bin instance
        """
        bin_ = await Bin.find(Bin.id == user_id).first_or_none()
        if bin_ is None:
            raise DBException(f"Cart for user {user_id} not found")
        return bin_
