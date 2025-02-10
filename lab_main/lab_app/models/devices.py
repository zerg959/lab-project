from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import (Column, Integer, String, Boolean,
                        CheckConstraint, ForeignKey, Float, Time)
from .base import Base

DEVICE_TYPE_SENSOR = "sensor"
DEVICE_TYPE_REGULATOR = "regulator"


class Device(Base):
    """
    Abstract class.
    Parent Device model for Sensor and Regulator models.
    to create Devices of different types: Sensors, Regulators etc.

    id (plymorphic id from children class): unique id of the device-type object.
    """
    # __abstract__ = True
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)

    description = Column(String, default="Device")
    """
    description (str): Device description. Default="device".
    """
    is_outdoor = Column(Boolean, default=False, nullable=False)
    """
    is_outdoor (bool): Device location flag - (indoor/outdoor). Default value = "False"
    """
    is_active = Column(Boolean, default=False, nullable=False)
    """
    is_active (bool): Device status (on/off). Default value = "False".
    """
    is_auto_mode_on = Column(Boolean, default=False, nullable=False)
    """
    auto_mode (bool): Device mode (on/off), to set automatic mode. Default value= "False".
    """
    auto_start_time = Column(Time, nullable=True)
    """
    auto_start_time (time): Devicec start time
    """
    device_type = Column(String,
                         CheckConstraint(
                             f'device_type IN ("{DEVICE_TYPE_SENSOR}",\
                                         "{DEVICE_TYPE_REGULATOR}")'
                                         ),
                         nullable=True,
                         )
    """
    device_type (str): Type of the Device (for ex.: sensor, regulator).
    Default value = DEVICE_TYPE_SENSOR.
    """
    @declared_attr
    def zone_id(cls):
        return Column(Integer, ForeignKey('zones.id'), nullable=True)

    @declared_attr
    def zone(cls):
        return relationship("Zone", back_populates="devices")
    """
    zone_id(int): ID of the linked Zone.
    """

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class Sensor(Device):
    """
    Sensor class.
    Sibling of the Device class.
    Use for parameters control: co2-, t-, humidity- sensors.
    """
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_SENSOR,
    }

    current_sensor_param = Column(Float,  nullable=True)
    """
    current_sensor_param: current value of param (default="N/A")
    """
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=True)
    parameter = relationship("Parameter",
                             back_populates="sensors",
                             )
    """
    parameter: Backref for linked Parameter.
    """

    def __repr__(self):
        return f"Parameter {self.id} : {self.description}>"


class Regulator(Device):
    """
    Regulator class.
    Sibling of the Device class.
    Use for parameter managing: co2-, t-, humidity- sensors.
    """
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_REGULATOR,
    }

    def __repr__(self):
        return f"Regulator {self.id}: {self.description}"
