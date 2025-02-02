import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from lab_main.lab_app.models.users import User, Base


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
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    assert session is not None


def test_user_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
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
