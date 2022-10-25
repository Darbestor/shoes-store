"""Response models for login"""

from uuid import UUID
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """Login response"""

    id: UUID | None = None
    username: str
