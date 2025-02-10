from sqlalchemy.orm import validates, relationship, declared_attr
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey, Float, Time
from .base import Base
from .storages import Storage
from .zones import Zone

DEVICE_TYPE_SENSOR="sensor"
DEVICE_TYPE_REGULATOR="regulator"

class Device(Base):
    """
    Abstract class.
    Parent Device model for Sensor and Regulator models.
    to create Deviceвs of different types: Sensors, Regulators etc.

    id (plymorphic id from children class): unique id of the device-type object.
    """
    __abstract__ = True
    # __tablename__ = "devices"
   
    id = Column(Integer, primary_key=True)
    # zone_id = Column(Integer, ForeignKey("zones.id"), nulllable=True, index=True)
    """
    zone_id(int): ID of the linked Zone.
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
    auto_start_time = Column(Time, nullable=True)
    """
    auto_start_time (time): Devicec start time
    """
    device_type = Column(String,
                         CheckConstraint(f'device_type IN ("{DEVICE_TYPE_SENSOR}", "{DEVICE_TYPE_REGULATOR}")'), 
                         nullable=True,
    )
    """
    device_type (str): Type of the Device (for ex.: sensor, regulator). Default value = DEVICE_TYPE_SENSOR.
    """

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
    

class Sensor(Device):
    """
    Sensor class.
    Sibling of the Device class.
    Use for parameters control: co2-, t-, humidity- sensors.
    :param: 
    :param: 

    """
    __tablename__ = "sensors"
    # id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
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
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=True)    
    zone = relationship("Zone", back_populates="sensors")
    """
    zone_id(int): ID of the linked Zone.
    """
    parameters = relationship("Parameter", back_populates="sensor")
    """
    parameter: Backref for linked Parameter.
    """

    # parameter_id = Column(Integer, ForeignKey("parameteres.id"), default="not set")
    # """
    # Linked Parameter ID.
    # """

    # @declared_attr
    # def zone(cls):
    # # zone = relationship("Zone", back_populates="devices")
    #     return relationship("Zone", back_populates="sensors")
    # """
    # zone: Backref for linked Zone.
    # """

    # def parameter(cls):
    #     return relationship("Parameter", back_populates="sensor")

    # parameter =  relationship("Parameter", back_populates="sensor")
    """
    Backref for "Parameter" in DB.
    """
    def __repr__(self):
        return f"Parameter {self.id} : {self.description}>"


class Regulator(Device):
    """
    Regulator class.
    Sibling of the Device class.
    Use for parameter managing: co2-, t-, humidity- sensors.
    """
    __tablename__ = "regulators"
    # id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_REGULATOR,
    }

    # @declared_attr
    # def zone(cls):
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=True)
    zone = relationship("Zone", back_populates="regulators")
        # return relationship("Zone", back_populates="regulators")
    """
    zone: Backref for linked Zone.
    """

    def __repr__(self):
        return f"Regulator {self.id}: {self.description}"
    