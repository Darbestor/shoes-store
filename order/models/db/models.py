"""Cart database document definitions"""

from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel


class Item(BaseModel):
    """Item in bin"""

    item_id: UUID
    quantity: int


class Order(Document):
    """Mongodb model"""

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    user_id: UUID = Field(default_factory=uuid4)  # type: ignore
    items: list[Item]
    address: str | None
    phone: int | None
    shipping_date: datetime | None
    total_price: float
    created_date: datetime

    class Settings:
        """settings"""

        name = "orders"
        indexes = [IndexModel("created_date", expireAfterSeconds=900)]
