from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from typing import List

# from datetime import datetime, timezone
from .base import Base


class Parameter(Base):
    """
    Represents a parameter that can be measured or managed by sensors or
    regulators, respectively.

    Attributes:
        id (int):
        Unique identifier for the parameter.
        parameter_name (Optional[str]):
        Name of the parameter (e.g., "temperature", "humidity").
        parameter_unit (Optional[str]):
        Unit of measurement for the parameter (e.g., "°C", "%"). Default=None.
        description (str): Description of the parameter. Default="parameter".
        sensors (List[:class:`Sensor`]):
        List of sensors associated with this parameter.
    """

    __tablename__ = "parameters"

    id: Column[int] = Column(Integer, primary_key=True)
    parameter_name: Column[str] = Column(String, nullable=True)
    parameter_unit: Column[str] = Column(String, nullable=True)
    description: Column[str] = Column(String, default="parameter")
    sensors = relationship(
        "Sensor",
        back_populates="parameter",
    )
    # timestamp = Column(DateTime,
    # default=datetime.datetime.now(timezone.utc)) # Date and time

    def __repr__(self):
        return f"Parameter id={self.id}, description: {self.description}"
