"""Cart database document definitions"""

from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field


class Item(BaseModel):
    """Item in bin"""

    item_id: UUID
    quantity: int


class Order(BaseModel):
    items: list[Item]
    address: str | None
    phone: int | None
    shipping_date: datetime | None
    total_price: float
    created_date: datetime


class OrderHistory(Document):
    """Mongodb model"""

    # user id
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    orders: list[Order]

    class Settings:
        """settings"""

        name = "order_history"
