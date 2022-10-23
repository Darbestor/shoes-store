"""Login model"""

from uuid import uuid4
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.db import orm_mapper


@orm_mapper.mapped
class Login:
    """Login table"""

    __tablename__ = "login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    passphrase = Column(LargeBinary)

    # one to one
    profile = relationship("Login", back_populates="login", uselist=False)
