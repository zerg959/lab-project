from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
# from datetime import datetime, timezone
from .base import Base


class Parameter(Base):
    """
    Parameter class.
    """
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True)

    parameter_name = Column(String, nullable=True)  # t или humidity
    parameter_unit = Column(String, nullable=True)
    description = Column(String, default="parameter")
    sensors = relationship("Sensor",
                           back_populates="parameter",
                          )
    # timestamp = Column(DateTime, default=datetime.datetime.now(timezone.utc)) # Date and time

    def __repr__(self):
        return f"Parameter: {self.id}, description: {self.description}"
