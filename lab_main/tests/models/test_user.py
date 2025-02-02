import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from lab_app.models.users import User, Base


def test_user_creates():
    """
    Tests if user created correctly.
    """
    user = User(name='Test user', email='mail@test.com')
    assert user.name == 'Test user'
    assert user.email == 'mail@test.com'
    assert user.role == 'user'
