"""Login request models"""

from uuid import UUID
from pydantic import BaseModel


class LoginReq(BaseModel):
    """Login request"""

    id: UUID | None = None
    username: str
    password: str
