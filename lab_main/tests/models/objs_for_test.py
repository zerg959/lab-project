from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from lab_main.lab_app.models.users import User
from lab_main.lab_app.models.storages import Storage
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
    """
    admin = User(
        name=name if name else fake.name(),
        email=email if email else fake.email(),
        role='admin'
    )
    return admin


def storage_for_tests(users=None, description=None):
    """
    Create storage for tests.
    """
    storage = Storage(
        users=users if users is not None else [],
        description=description if description else fake.sentence()
    )
    return storage
