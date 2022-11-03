from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass
class OrderCreate:
    user_id: UUID
    items: dict[UUID, int]
