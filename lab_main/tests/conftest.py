import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from lab_main.lab_app.models.base import Base
from lab_main.lab_app.models import (User, Storage, Zone,
                                     Parameter, Sensor, Regulator)

fake = Faker()

@pytest.fixture(scope="session")
def engine():
    """Yields a SQLAlchemy engine which is suppressed after the test session"""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def session(engine, create_tables):
    """Yields a SQLAlchemy connection which is rollbacked after the test function"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=engine)
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_user():
    return MagicMock(spec=User)

@pytest.fixture
def mock_admin():
    mock = MagicMock(spec=User)
    mock.role = "admin"
    return mock

@pytest.fixture
def mock_storage():
    return MagicMock(spec=Storage)

@pytest.fixture
def mock_zone():
    return MagicMock(spec=Zone)

@pytest.fixture
def mock_sensor():
    return MagicMock(spec=Sensor)

@pytest.fixture
def mock_regulator():
    return MagicMock(spec=Regulator)

@pytest.fixture
def mock_param():
    return MagicMock(spec=Parameter)


@pytest.fixture()
def storage_for_tests():
    """Create storage for tests."""
    def _storage_for_tests(users=None, zones=None, description=None):
        storage = Storage(
            users=users if users is not None else [],
            zones=zones if zones is not None else [],
            description=description if description else fake.sentence(),
        )
        return storage
    return _storage_for_tests


@pytest.fixture()
def zone_for_tests():
    """Create zone for tests."""
    def _zone_for_tests(storage=None, description=None):
        zone = Zone(description=description if description else fake.sentence())
        return zone
    return _zone_for_tests


@pytest.fixture()
def user_for_tests():
    """Create user for tests."""
    def _user_for_tests(name=None, email=None, role=None):
        user = User(
            name=name if name else fake.name(),
            email=email if email else fake.email(),
            role=role,
        )
        return user
    return _user_for_tests


@pytest.fixture()
def admin_for_tests():
    """Create admin for tests."""
    def _admin_for_tests(name=None, email=None):
        admin = User(
            name=name if name else fake.name(),
            email=email if email else fake.email(),
            role="admin",
        )
        return admin
    return _admin_for_tests


@pytest.fixture()
def sensor_for_tests():
    """Create sensor for tests."""
    def _sensor_for_tests(zone=None, description=None, is_outdoor=False,
                          is_auto_mode_on=False, device_type='sensor',):
        if device_type not in ['sensor', 'regulator']:
            raise ValueError("Invalid device_type.\
                             Must be 'sensor' or 'regulator'.")
        sensor = Sensor(
            zone=zone,
            description=description if description else fake.sentence(),
            is_outdoor=is_outdoor,
            is_auto_mode_on=is_auto_mode_on,
            device_type=device_type,
            current_sensor_param=33.0,
            )
        return sensor
    return _sensor_for_tests


@pytest.fixture()
def regulator_for_tests():
    """Create sensor for tests."""
    def _regulator_for_tests(zone=None, description=None, is_outdoor=False,
                             is_auto_mode_on=False, device_type='regulator',):
        if device_type not in ['sensor', 'regulator']:
            raise ValueError("Invalid device_type.\
                             Must be 'sensor' or 'regulator'.")
        regulator = Regulator(
            zone=zone,
            description=description if description else fake.sentence(),
            is_outdoor=is_outdoor,
            is_auto_mode_on=is_auto_mode_on,
            device_type=device_type,
            )
        return regulator
    return _regulator_for_tests


@pytest.fixture()
def param_for_tests():
    """Create param for tests."""
    def _param_for_tests(sensors=None, parameter_name=None,
                         parameter_unit=None, description=None):
        parameter = Parameter(sensors=sensors if sensors else [],
                              parameter_name=parameter_name if
                              parameter_name else 'no data',
                              parameter_unit=parameter_unit if
                              parameter_unit else 'no data',
                              description=description if description else '',
                              )
        return parameter
    return _param_for_tests

    # id = Column(Integer, primary_key=True)
    # sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)  # Required!
    # sensor = relationship("Sensor", back_populates="parameters")
    # parameter_name = Column(String, nullable=False) # t или humidity
    # current_value = Column(Float, nullable=True)
    # description = Column(String, default="parameter")