from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey, Float
from .base import Base
from .storages import Storage

DEVICE_TYPE_SENSOR="sensor"
DEVICE_TYPE_REGULATOR="regulator"

class Device(Base):
    """
    Abstract class.
    Parent Device model for Sensor and Regulator models.
    to create Devices of different types: Sensors, Regulators etc.
    Attributes:
    id (plymorphic id from children class): unique id of the device-type object.
    zone_id(int): ID of the linked Zone.
    description (str): Device description. Default="device".
    is_active (bool): Device status (on/off). Default value = "False".
    is_outdoor (bool): Device loctation flag - (indoor/outdoor). Default value = "False"
    device_type (str): Type of the Device (for ex.: sensor, regulator). Default value = DEVICE_TYPE_SENSOR.

    """
    __abstract__ = True
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=True)
    zone = relationship("Zone", back_populates="devices")
    description = Column(String, default='Device')
    is_active = Column(Boolean, default=False, nullable=False)
    is_outdoor = Column(Boolean, default=False, nullable=False)
    device_type = Column(String,
                         CheckConstraint(f'device_type IN ("{DEVICE_TYPE_SENSOR}", "{DEVICE_TYPE_REGULATOR}")'), 
                         default=DEVICE_TYPE_SENSOR, 
                         nullable=False,
    )



class Sensor(Device):
    """
    Sensor class.
    Sibling of the Device class.
    Use for integration of measurement devices: co2-, t-, humidity- sensors.
    """
    __tablename__ = "sensors"
    id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_SENSOR,
    }
    current_sensor_param = Column(Float, defaulr='N/A', nullable=True)

    def __repr__(self):
        return f"Sensor {self.id}: {self.description}"
