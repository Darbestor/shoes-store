"""Request models for Model document"""

from pydantic import BaseModel

from models.common.color import Color
from models.common.gender import Gender
from models.common.sport_type import SportType


class CreateModelReq(BaseModel):
    """Request to add new model"""

    name: str
    description: str
    size: float
    quantity: int
    sport_type: SportType
    company: str
    collection: str
    color: Color
    gender: Gender
