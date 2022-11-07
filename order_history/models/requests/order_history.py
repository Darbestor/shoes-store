from uuid import UUID
from pydantic import BaseModel

from models.db.models import Order


class OrderReq(BaseModel):
    user_id: UUID
    order: Order
