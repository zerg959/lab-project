# from sqlalchemy import create_engine
# from lab_main.lab_app.models.base import Base
# from .objs_for_test import *


# engine = create_engine("sqlite:///:memory:")
# session = db_for_tests(engine)

# def test_sensor():
#     # storage = storage_for_tests()
#     # zone = zone_for_tests()
#     sensor = sensor_for_tests()
#     param = param_for_tests()
#     session.add_all([sensor, param])
#     # session.add_all([storage, zone, sensor])
#     session.commit()
#     assert sensor.id is not None
#     session.close()
#     Base.metadata.drop_all(engine)
import pytest
from pytest.fixtures import fixtures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lab_main.lab_app.models.devices import Sensor, Device
from lab_main.lab_app.models.zones import Zone
from lab_main.lab_app.models.base import Base

# Создание временной базы данных для тестов

@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def test_sensor_creation(session):
    """
    Проверяет создание объекта Sensor.
    """
    sensor = Sensor(
        description="Test Sensor",
        is_outdoor=False,
        is_active=True,
        is_auto_mode_on=False,
        current_sensor_param=25.5,
    )
    session.add(sensor)
    session.commit()

    # Проверяем, что объект создан и добавлен в базу данных
    assert sensor.id is not None
    assert sensor.description == "Test Sensor"
    assert sensor.is_outdoor is False
    assert sensor.is_active is True
    assert sensor.current_sensor_param == 25.5

def test_sensor_relationship_with_zone(session):
    """
    Проверяет связь Sensor с Zone.
    """
    zone = Zone(description="Test Zone")
    session.add(zone)
    session.commit()

    sensor = Sensor(
        description="Sensor in Test Zone",
        is_outdoor=False,
        is_active=True,
        zone_id=zone.id,
    )
    session.add(sensor)
    session.commit()

    # Проверяем, что связь установлена корректно
    assert sensor.zone_id == zone.id