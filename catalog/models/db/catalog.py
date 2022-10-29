"""Catalog document definition"""

from uuid import UUID, uuid4
from beanie import Document, Link
from pydantic import BaseModel, Field
from pymongo import IndexModel
import pymongo

from models.common.color import Color
from models.common.gender import Gender
from models.common.sport_type import SportType


class Details(BaseModel):
    """Additional information about model"""

    sport_type: SportType
    company: str
    collection: str
    color: Color
    gender: Gender


class Warehouse(Document):
    """Models management storage"""

    model_id: UUID  # type: ignore
    storage: dict[float, int]

    class Settings:
        """settings"""

        name = "warehouse"


class Model(Document):
    """Mongodb model"""

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    name: str
    description: str
    price: float
    details: Details
    storage: Link[Warehouse]

    class Settings:
        """settings"""

        name = "model"
        indexes = [
            IndexModel(
                [("name", pymongo.TEXT)],
            ),
            "price",
            [
                ("details.sport_type", pymongo.ASCENDING),
                ("details.company", pymongo.ASCENDING),
            ],
        ]
