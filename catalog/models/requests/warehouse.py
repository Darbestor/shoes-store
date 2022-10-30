"""Warehouse requests"""

from fastapi import Form
from pydantic import BaseModel, validator


class WarehouseReq(BaseModel):
    """Request payload"""

    size: int
    quantity: int

    @validator("size")
    def greater_than_zero(cls, value):  # pylint: disable=E0213
        if value <= 0:
            raise ValueError("Size must be grater than 0.")
        return value

    @classmethod
    def as_form(
        cls,
        size: int = Form(...),
        quantity: int = Form(...),
    ):
        """Represent object parameters as Form parameters"""
        return cls(size=size, quantity=quantity)
