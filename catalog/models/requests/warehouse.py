"""Warehouse requests"""

from pydantic import BaseModel, validator


class WarehouseReq(BaseModel):
    """Request payload"""

    size: float
    quantity: int

    @validator("*")
    def greater_than_zero(cls, value):  # pylint: disable=E0213
        assert value > 0
