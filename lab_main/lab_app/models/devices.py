from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey, Float, Time
from .base import Base
from .storages import Storage

DEVICE_TYPE_SENSOR="sensor"
DEVICE_TYPE_REGULATOR="regulator"

class Device(Base):
    """
    Abstract class.
    Parent Device model for Sensor and Regulator models.
    to create Devices of different types: Sensors, Regulators etc.

    id (plymorphic id from children class): unique id of the device-type object.
    """
    __abstract__ = True
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=True)
    """
    zone_id(int): ID of the linked Zone.
    """
    zone = relationship("Zone", back_populates="devices")
    """
    zone: Backref for linked Zone.
    """
    description = Column(String, default='Device')
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
    auto_start_time = Column(Time, nullable=True) # Добавил время
    device_type = Column(String,
                         CheckConstraint(f'device_type IN ("{DEVICE_TYPE_SENSOR}", "{DEVICE_TYPE_REGULATOR}")'), 
                         default=DEVICE_TYPE_SENSOR, 
                         nullable=False,
    )
    """
    device_type (str): Type of the Device (for ex.: sensor, regulator). Default value = DEVICE_TYPE_SENSOR.
    """



class Sensor(Device):
    """
    Sensor class.
    Sibling of the Device class.
    Use for parameters control: co2-, t-, humidity- sensors.
    :param: 
    :param: 

    """
    __tablename__ = "sensors"
    id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_SENSOR,
    }
    """
    id (plymorphic id from children class): unique id of the device-type object. Also used as Device-ID.
    """
    current_sensor_param = Column(Float,  nullable=True)
    """
    current_sensor_param: current value of param (default="N/A")
    """
    # parameter_id = Column(Integer, ForeignKey("parameteres.id"), default="not set")
    # """
    # Linked Parameter ID.
    # """
    parameter =  relationship("Parameter", back_populates="sensor")
    """
    Backref for "Parameter" in DB.
    """


    def __repr__(self):
        return f"Sensor {self.id}: {self.description}"


class Regulator(Device):
    """
    Regulator class.
    Sibling of the Device class.
    Use for parameter managing: co2-, t-, humidity- sensors.
    """
    __tablename__ = "regulators"
    id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_REGULATOR,
    }


    def __repr__(self):
        return f"Regulator {self.id}: {self.description}"