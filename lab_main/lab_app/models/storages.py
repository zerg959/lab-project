from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from typing import List
from .associations import association_table
from .base import Base


class Storage(Base):
    """
      Represents a storage area with associated zones and users.

      A storage area can contain multiple zones with different environmental
      conditions.
      Multiple users can be authorized to manage a storage area.

      Attributes:
          id (int):
          Unique identifier for the storage area.
          description (Optional[str]):
          Description of the storage area.
          users (List[:class:`User`]):
          List of users who have access to manage this storage area.
          The relationship is many-to-many via the `association_table`.
          zones (List[:class:`Zone`]):
          List of zones contained within this storage area.
      """
    __tablename__ = "storages"
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User",
                        secondary=association_table,
                        back_populates="storages"
                        )
    zones = relationship("Zone", back_populates="storage")

    def __repr__(self):
        return f"Storage id={self.id}: {self.description}"
