"""Profile model"""

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.db import Base
from .login import Login


class Profile(Base):
    """Profile table"""

    __tablename__ = "profile"

    login_id = Column(UUID(as_uuid=True), ForeignKey(Login.id), primary_key=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    middlename = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_date = Column(DateTime(timezone=False), nullable=False)
    modified_date = Column(DateTime(timezone=False), nullable=False)

    # many to one, but has to be only one login associated
    login = relationship("Login", back_populates="profile")
