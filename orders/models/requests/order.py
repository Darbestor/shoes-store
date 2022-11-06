from datetime import datetime
from uuid import UUID
from fastapi import Form, Query
from pydantic import BaseModel


class OrderInfoReq(BaseModel):
    order_id: UUID = Query(...)
    address: str
    phone: int
    shipping_date: datetime

    @classmethod
    def as_form(
        cls,
        order_id=Query(...),
        address: str = Form(...),
        phone: int = Form(...),
        shipping_date: datetime = Form(...),
    ):
        return cls(
            order_id=order_id, address=address, phone=phone, shipping_date=shipping_date
        )
