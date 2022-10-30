from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, validator


class BinReq(BaseModel):
    user_id: UUID = Query(...)
    item_id: UUID = Query(...)
    quantity: int = Query(...)

    @validator("quantity")
    def greater_than_zero(cls, value):  # pylint: disable=E0213
        if value < 1:
            raise ValueError("Size must be grater than 0")
        return value
