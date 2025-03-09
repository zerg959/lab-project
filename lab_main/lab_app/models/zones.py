from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import List
from .base import Base


class Zone(Base):
    """
    Represents a zone within a storage area, containing a specific set of
    sensors and regulators.

    A storage area can contain multiple zones, each with potentially different
    environmental conditions.

    Attributes:
      - id (int): Unique identifier for the zone.
      - storage_id (Optional[int]): ForeignKey referencing the
            :class:`Storage` object this zone belongs to.
        storage (:class:`Storage`): Relationship to the :class:`Storage`
            object this zone belongs to.
      - devices (List[:class:`Device`]): List of devices (sensors and
            regulators) associated with this zone.
      - description (str): Description of the zone. Defaults to "zone".
    """

    __tablename__ = "zones"
    id: Column[int] = Column(Integer, primary_key=True)
    storage_id: Column[int] = Column(
        Integer,
        ForeignKey("storages.id"),
        nullable=True, index=True
        )
    storage = relationship("Storage", back_populates="zones")
    devices = relationship("Device", back_populates="zone")
    description: Column[str] = Column(String, default="zone")
    # internal_cur_params =
    # internal_avg_params =
    # external_cur_params =
    # internal_avg_params =
    # min_params =
    # max_params =

    def __repr__(self):
        return f"Zone id={self.id}: {self.description}"
