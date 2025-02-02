import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from lab_main.lab_app.models.users import User, Base


def db_created():
    """
    Create DB.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_user_creates():
    """
    Tests if user created correctly. And if role is None used defaul value 'user'.
    """
    user = User(name='Test user', email='mail@test.com', role=None)
    assert user.name == 'Test user'
    assert user.email == 'mail@test.com'
    assert user.role == 'user'


def test_db_created():
    """
    Tests if Sqlite DB created successfully.
    """
    session = db_created()
    assert session is not None


def test_user_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    session = db_created()
    user = User(name='Test user', email='mail@test.com')
    session.add(user)
    session.commit()
    test_user_from_db = session.query(User).filter_by(
        email='mail@test.com'
        ).first()
    assert test_user_from_db is not None
    assert test_user_from_db.name == 'Test user'
    assert test_user_from_db.email == 'mail@test.com'
    assert test_user_from_db.role == 'user'
    assert test_user_from_db.id == 1


def test_admin_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    session = db_created()
    user = User(name='Test admin', email='mail@test.com', role='admin')
    session.add(user)
    session.commit()

    test_user_from_db = session.query(User).filter_by(
        email='mail@test.com'
        ).first()
    assert test_user_from_db is not None
    assert test_user_from_db.name == 'Test admin'
    assert test_user_from_db.email == 'mail@test.com'
    assert test_user_from_db.role == 'admin'
    assert test_user_from_db.id == 1
