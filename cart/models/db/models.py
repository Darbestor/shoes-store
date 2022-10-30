"""Cart database document definitions"""

from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field


class Item(BaseModel):
    """Item in bin"""

    model_id: UUID
    quantity: int


class Bin(Document):
    """Mongodb model"""

    # id is user id. Because cart is only 1 for user
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    items: list[Item]

    class Settings:
        """settings"""

        name = "bin"
