from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from lab_main.lab_app.models.users import User
from lab_main.lab_app.models.storages import Storage
from lab_main.lab_app.models.zones import Zone
from lab_main.lab_app.models.base import Base

fake = Faker()


def db_for_tests():
    """
    Create DB for tests.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def user_for_tests(name=None, email=None, role=None):
    """
    Create user for tests.
    :param name: Optional User name.
    :param email: Optional email param to set own email.
    """
    user = User(
        name=name if name else fake.name(),
        email=email if email else fake.email(),
        role=role
    )
    return user


def admin_for_tests(name=None, email=None):
    """
    Create admin for tests.
    :param name: Optional User name.
    :param email: Optional email param to set own email.
    """
    admin = User(
        name=name if name else fake.name(),
        email=email if email else fake.email(),
        role='admin'
    )
    return admin


def storage_for_tests(users=None, zones=None, description=None):
    """
    Create storage for tests.
    :param users: Optional User object to associate with the Storage.
    :param zones: Optional Zone object to associate with the Storage.
    :param description: Description of the Storage.
    
    """
    storage = Storage(
        users=users if users is not None else [],
        zones=zones if zones is not None else [],
        description=description if description else fake.sentence()
    )
    return storage

def zone_for_tests(storage=None, description=None):
    """
    Create zone for tests.
    :param storage: Optional Storage object to associate with the Zone.
    :param description: Description of the Zone.
    """
    storage=storage,
    zone = Zone(
        description=description if description else fake.sentence()
    )
    return zone
