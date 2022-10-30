"""Request models for Model document"""

from typing import Union
from fastapi import Form
from pydantic import BaseModel

from models.common.color import Color
from models.common.gender import Gender
from models.common.sport_type import SportType


class ModelReq(BaseModel):
    """Base request for model"""

    name: str
    description: str
    sport_type: SportType
    company: str
    collection: str
    color: Color
    gender: Gender

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        sport_type: SportType = Form(...),
        company: str = Form(...),
        collection: str = Form(...),
        color: Color = Form(...),
        gender: Gender = Form(...),
    ):
        """Represent object parameters as Form parameters"""
        return cls(
            name=name,
            description=description,
            sport_type=sport_type,
            company=company,
            collection=collection,
            color=color,
            gender=gender,
        )


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
