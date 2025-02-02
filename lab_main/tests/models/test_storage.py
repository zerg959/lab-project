from lab_main.lab_app.models.storages import Storage
from lab_main.lab_app.models.users import User
from . objs_for_test import user_for_tests, db_for_tests


def test_storage_created():
    """
    Test if storage created in DB with params.
    """
    user = user_for_tests()
    storage = Storage(user_id=user.id, description='Test storage description')
    assert storage.user_id == user.id
    assert storage.description == 'Test storage description'


def test_storage_recorded_in_DB():
    """
    Test if storage recorded in DB.
    """
    db = db_for_tests()
    user1 = user_for_tests()
    user2 = user_for_tests()
    user2.email = 'mail2@test.com'
    db.add(user1)
    db.add(user2)
    db.commit()
    storage = Storage(description='Test storage description')
    storage.users.append(user1)
    storage.users.append(user2)
    db.add(storage)
    db.commit()
    test_storage_from_db = db.query(Storage).filter_by(
        description='Test storage description'
        ).first()
    assert test_storage_from_db is not None
    assert test_storage_from_db.id is not None
    assert test_storage_from_db.description == 'Test storage description'
    assert len(test_storage_from_db.users) == 2
    assert user1 in test_storage_from_db.users
    assert user2 in test_storage_from_db.users

def test_user_storages_recorded_in_DB():
        """
        Test if user storages recorded in DB.
        """
        db = db_for_tests()
        user = user_for_tests()
        db.add(user)
        db.commit()
        storage1 = Storage(description='Test storage description 1')
        storage2 = Storage(description='Test storage description 2')
        storage1.users.append(user)
        storage2.users.append(user)
        db.add(storage1)
        db.add(storage2)
        db.commit()
        test_user_from_db = db.query(User).filter_by(
             email='mail@test.com'
            ).first()
        assert test_user_from_db is not None
        assert test_user_from_db.id is not None
        assert len(test_user_from_db.storages) == 2
        assert storage1 in test_user_from_db.storages
        assert storage2 in test_user_from_db.storages
