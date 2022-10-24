"""Login request models"""

from pydantic import BaseModel


class LoginReq(BaseModel):
    """Login request"""

    username: str
    password: str
