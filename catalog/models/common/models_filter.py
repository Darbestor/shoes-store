"""Model filtering"""


from typing import Union
from pydantic import BaseModel
from .sport_type import SportType
from .color import Color
from .gender import Gender


class ModelFilter(BaseModel):
    """Filtering models"""

    name: str | None
    size: float | None
    sport_type: SportType | None
    company: str | None
    collection: str | None
    color: Color | None
    gender: Gender | None
    price_range: Union[float, float]
