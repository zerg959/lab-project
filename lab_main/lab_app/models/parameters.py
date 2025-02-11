from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

# from datetime import datetime, timezone
from .base import Base


class Parameter(Base):
    """
    Parameter class.
    """

    __tablename__ = "parameters"
    """
    tablename: DB-table name.
    """
    id = Column(Integer, primary_key=True)
    """
    id (int): Parameter-object ID.
    """
    parameter_name = Column(String, nullable=True)
    """
    parameter_name (str): name of the parameter
    (for ex: temperature, humidity). Default: None.
    """
    parameter_unit = Column(String, nullable=True)
    """
    parameter_unit (str): parameter unit. Default: None.
    """
    description = Column(String, default="parameter")
    """
    description (str): parameter description. Default: None.
    """
    sensors = relationship(
        "Sensor",
        back_populates="parameter",
    )
    """
    sensors (list): list of linked sensors.
    """
    # timestamp = Column(DateTime,
    # default=datetime.datetime.now(timezone.utc)) # Date and time

    def __repr__(self):
        return f"Parameter: {self.id}, description: {self.description}"
