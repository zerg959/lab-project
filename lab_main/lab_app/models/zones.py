from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


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
    """
    id (int): zone ID in DB.
    """
    storage_id = Column(Integer,
                        ForeignKey("storages.id"),
                        nullable=True, index=True
                        )
    """
    storage_id (int): storage ID where zone is created.
    """
    storage = relationship("Storage", back_populates="zones")
    """
    storage (obj): Storage object linked with zone.
    """
    devices = relationship("Device", back_populates="zone")
    """
    devices (list): Device siblings objects
    (Regulator, Sensor) linked with zone.
    """
    description = Column(String, default="zone")
    """
    description (str): zone description. Default: zone.
    """

    # internal_cur_params =
    # internal_avg_params =
    # external_cur_params =
    # internal_avg_params =
    # min_params =
    # max_params =

    def __repr__(self):
        return f"Zone {self.id}: {self.description}"
