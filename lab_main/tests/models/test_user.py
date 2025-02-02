from . objs_for_test import db_for_tests, user_for_tests, admin_for_tests
from lab_main.lab_app.models.users import User


def test_db_created():
    """
    Tests if Sqlite DB created successfully.
    """
    session = db_for_tests()
    assert session is not None


def test_user_created():
    """
    Tests if user created correctly. And if role is None used defaul value 'user'.
    """
    user = user_for_tests()
    assert user.name == 'Test user'
    assert user.email == 'mail@test.com'
    assert user.role == 'user'


def test_user_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    session = db_for_tests()
    user = user_for_tests()
    session.add(user)
    session.commit()
    test_user_from_db = session.query(User).filter_by(
        email='mail@test.com'
        ).first()
    assert test_user_from_db is not None
    assert test_user_from_db.id is not None
    assert test_user_from_db.name == 'Test user'
    assert test_user_from_db.email == 'mail@test.com'
    assert test_user_from_db.role == 'user'
    assert test_user_from_db.id == user.id


def test_admin_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    session = db_for_tests()
    admin = admin_for_tests()
    session.add(admin)
    session.commit()

    test_admin_from_db = session.query(User).filter_by(
        email='mail@test.com'
        ).first()
    assert test_admin_from_db is not None
    assert test_admin_from_db.name == 'Test admin'
    assert test_admin_from_db.email == 'mail@test.com'
    assert test_admin_from_db.role == 'admin'
    assert test_admin_from_db.id == admin.id
