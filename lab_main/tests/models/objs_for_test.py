from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lab_main.lab_app.models.users import User, Base
# from lab_main.lab_app.models.storages import Storage


def db_for_tests():
    """
    Create DB for tests.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def user_for_tests():
    """
    Create user for tests.
    """
    user = User(name='Test user', email='mail@test.com', role=None)
    return user


def admin_for_tests():
    """
    Create admin for tests.
    """
    admin = User(name='Test admin', email='mail@test.com', role='admin')
    return admin


# def storage_for_tests():
#     storage = Storage(user_id=user_for_tests.id, description=None)
#     return storage