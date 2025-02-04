from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from .base import Base
from .storages import Storage


class Zone(Base):
    """
    Zone model:
    to create Zone with different set of Sensors and Regulators.
    In one Storage can be multiply Zones.
    Attributes:
    id (int): Unique zone ID.
    storage_id (int): ID of the linked Storage.
    description (str): Zone description.
    storage: Linked Storage.
    """

    __tablename__ = "zones"
    id = Column(Integer, primary_key=True)
    storage_id = Column(Integer, ForeignKey("storages.id"), nullable=True, index=True)
    description = Column(String, default="zone")
    storage = relationship("Storage", back_populates="zones")

    def __repr__(self):
        return f"Zone {self.id}: {self.description}"
