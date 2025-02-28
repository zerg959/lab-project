from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from .associations import association_table
from .base import Base


class Storage(Base):
    """
    Storage model:
    to create Storage with Zones.
    One Storage can be managed by multiply Users.
    Attributes:
    id (int): Unique storage ID.
    description (str): Storage description.
    users (list): Linked users.
    zones (list): Store zones.

    """

    __tablename__ = "storages"
    id = Column(Integer, primary_key=True, nullable=False)
    """
    id (int): Storage ID in DB.
    """
    description = Column(String, nullable=True)
    """
    description (str): Storage description.
    """
    users = relationship("User",
                         secondary=association_table,
                         back_populates="storages"
                         )
    """
    users (list): Users who can manage Storage.
    """
    zones = relationship("Zone", back_populates="storage")
    """
    zones (list): Zones for different conditions added in Storage.
    """

    def __repr__(self):
        return f"Storage {self.id}: {self.description}"
