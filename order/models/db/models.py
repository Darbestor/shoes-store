"""Cart database document definitions"""

from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field


class Item(BaseModel):
    """Item in bin"""

    item_id: UUID
    quantity: int


class Order(Document):
    """Mongodb model"""

    user_id: UUID = Field(default_factory=uuid4)  # type: ignore
    items: list[Item]
    address: str
    phone: int
    shipping_date: datetime

    class Settings:
        """settings"""

        name = "orders"
        indexes = ["user_id"]
