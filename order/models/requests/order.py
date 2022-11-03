from datetime import datetime
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel


class OrderInfoReq(BaseModel):
    order_id: UUID = Query(...)
    address: str
    phone: int
    shipping_date: datetime
