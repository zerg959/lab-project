from .objs_for_test import db_for_tests, user_for_tests, admin_for_tests
from lab_main.lab_app.models.users import User

session = db_for_tests()  # Create db session


def test_db_created():
    """
    Tests if Sqlite DB created successfully.
    """
    assert session is not None


def test_user_created():
    """
    Tests if user created correctly.
    If role is None used defaul value 'user'.
    """
    user = user_for_tests()
    session.add(user)
    session.commit()
    assert user.name is not None
    assert user.email is not None
    assert user.role == "user"
    assert user.storages == []


def test_user_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    user = user_for_tests()
    session.add(user)
    session.commit()
    user_from_bd = session.query(User).filter_by(id=user.id).first()
    assert user_from_bd.id == user.id
    assert user_from_bd.name == user.name
    assert user_from_bd.email == user.email
    assert user_from_bd.role == "user"
    assert len(user_from_bd.storages) == 0


def test_admin_recorded_in_DB():
    """
    Tests if user created in DB.
    """
    admin = admin_for_tests()
    session.add(admin)
    session.commit()
    admin_from_bd = session.query(User).filter_by(id=admin.id).first()
    assert admin_from_bd.id == admin.id
    assert admin_from_bd.name == admin.name
    assert admin_from_bd.email == admin.email
    assert admin_from_bd.role == "admin"
    assert len(admin_from_bd.storages) == 0
