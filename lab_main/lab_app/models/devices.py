from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Float,
    Time,
)
from .base import Base

DEVICE_TYPE_SENSOR = "sensor"
DEVICE_TYPE_REGULATOR = "regulator"


class Device(Base):
    """
    Parent Device model for Sensor and Regulator models.
    This class serves as a base for creating different
    types of devices, such as Sensors and Regulators.

    Attributes:
      - id (int): Unique device-ID.
      - description (str): Device description. Default="device"
        (f.ex.: "humidity sensor').
      - is_outdoor (bool): Device location flag - (indoor/outdoor).
        Default value = False.
      - is_active (bool): Device status (on/off). Default value = False.
      - is_auto_mode_on (bool): Device mode (on/off), enabling automatic
            operation. Default value= False.
      - auto_start_time (Optional[datetime.time]): Device's start time,
        or None if not set.
      - device_type (str): Type of the Device (for ex.: sensor, regulator).
        Limited by a CHECK constraint in the database.
        Default: :data:`DEVICE_TYPE_SENSOR`.
        Allowed values: :data:`DEVICE_TYPE_SENSOR`,
        :data:`DEVICE_TYPE_REGULATOR`.
      - zone_id (Optional[int]):  *Sensor/Regulator only.* ForeignKey
            referencing :class:`Zone`.id. Connects the device
            to a specific zone.
      - zone (Optional[Zone]): *Sensor/Regulator only.* Relationship to the
            :class:`Zone` object. Allows access to the associated zone.
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    description = Column(String, default="Device")
    is_outdoor = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_auto_mode_on = Column(Boolean, default=False, nullable=False)
    auto_start_time = Column(Time, nullable=True)
    device_type = Column(
        String,
        CheckConstraint(
            f'device_type IN ("{DEVICE_TYPE_SENSOR}",\
                                         "{DEVICE_TYPE_REGULATOR}")'
        ),
        default=DEVICE_TYPE_SENSOR,
        nullable=False,
    )

    @declared_attr
    def zone_id(cls):
        """
        (Sensor/Regulator only) ForeignKey referencing the Zone.id.
        Connects the device to a specific Zone.
        """
        return Column(Integer, ForeignKey("zones.id"), nullable=True)

    @declared_attr
    def zone(cls):
        """
        (Sensor/Regulator only) Relationship to the Zone object.
        Allows access to the associated Zone.
        """
        return relationship("Zone", back_populates="devices")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class Sensor(Device):
    """
    Represents a Sensor device, inheriting from the :class:`Device` model.

    This class is used to represent sensors that monitor various parameters
    like CO2 levels, temperature, and humidity.
    It's a sibling class to other device types like :class:`Regulator`.

    Attributes:
        current_sensor_param (Optional[float]):
        The current value of the parameter being measured by the sensor.
        Can be None if no reading is available.
        parameter_id (Optional[int]):
        ForeignKey referencing the :class:`Parameter` object associated
        with this sensor.
        parameter (:class:`Parameter`):
        Relationship to the associated :class:`Parameter` object.
        Provides access to the parameter's details.
    """

    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_SENSOR,
    }

    current_sensor_param = Column(Float, nullable=True)
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=True)
    parameter = relationship(
        "Parameter",
        back_populates="sensors",
    )

    def __repr__(self):
        return f"Sensor id={self.id} : {self.description}>"


class Regulator(Device):
    """
    Represents a Regulator device, inheriting from the :class:`Device` model.
    This class is used to represent regulators that manage various parameters
    like CO2 levels, temperature, and humidity.
    It's a sibling class to other device types like :class:`Sensor`.
    """

    __mapper_args__ = {
        "polymorphic_identity": DEVICE_TYPE_REGULATOR,
    }

    def __repr__(self):
        return f"Regulator id={self.id}: {self.description}"
