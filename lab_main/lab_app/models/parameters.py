from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey, Float, Time, DateTime
from datetime import datetime, timezone
from .base import Base
from .devices import Sensor, Regulator
from .storages import Storage


class Parameter(Base):
    """
    Parameter class.
    """
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)  # Required!
    sensor = relationship("Sensor", back_populates="parameters")
    parameter_name = Column(String, nullable=False) # t или humidity
    current_value = Column(Float, nullable=True)
    description = Column(String, default="parameter")
    # timestamp = Column(DateTime, default=datetime.datetime.now(timezone.utc)) # Date and time

    def __repr__(self):
        return f"Parameter(id={self.id}, name={self.parameter_name}, value={self.current_value})"