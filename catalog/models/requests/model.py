"""Request models for Model document"""

from typing import Union
from pydantic import BaseModel

from models.common.color import Color
from models.common.gender import Gender
from models.common.sport_type import SportType


class CreateModelReq(BaseModel):
    """Request to add new model"""

    name: str
    description: str
    sport_type: SportType
    company: str
    collection: str
    color: Color
    gender: Gender


class ModelFilterReq(BaseModel):
    """Filtering models"""

    name: str | None
    size: float | None
    sport_type: SportType | None
    company: str | None
    collection: str | None
    color: Color | None
    gender: Gender | None
    price_range: Union[float, float]
