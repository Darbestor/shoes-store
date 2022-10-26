"""Catalog document definition"""

from enum import Enum, IntEnum
from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel
import pymongo


class Gender(IntEnum):
    """Gender"""

    M = 0
    F = 1
    U = 2


class SportType(str, Enum):
    """Sport type for shoes"""

    FOOTBALL = "football"
    BASKETBALL = "basketball"
    WALKING = "walking"
    RUNNING = "running"
    LIFESTYLE = "lifestyle"


class Color(str, Enum):
    """Shoes colors"""

    BLUE = "blue"
    GREEN = "green"
    BLACK = "black"
    WHITE = "white"


class Details(BaseModel):
    """Additional information about model"""

    sport_type: SportType
    company: str
    collection: str
    color: Color
    gender: Gender


class Model(Document):
    """Mongodb model"""

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    name: str
    description: str
    sizes: dict[float, int]
    price: float
    details: Details

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
