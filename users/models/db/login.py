"""Login model"""

from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.db import Base


if TYPE_CHECKING:
    from . import Profile


class Login(Base):
    """Login table"""

    __tablename__ = "login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: str = Column(String, unique=True, index=True, nullable=False)
    passphrase: bytes = Column(LargeBinary, nullable=False)

    # one to one
    profile: Profile = relationship("Profile", back_populates="login", uselist=False)
