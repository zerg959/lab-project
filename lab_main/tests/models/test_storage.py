from lab_main.lab_app.models.storages import Storage, association_table
from lab_main.lab_app.models.users import User
from . objs_for_test import user_for_tests, db_for_tests, storage_for_tests

session = db_for_tests()  # Create db session

def test_storage_created():
    """
    Test if storage created in DB with params.
    """
    storage = storage_for_tests()
    session.commit()
    assert storage.description is not None
    assert storage.users == []

def test_storage_recorded_in_DB():
    """
    Test if storage recorded in DB.
    """
    user1 = user_for_tests()
    storage = storage_for_tests(users=[user1])
    session.add(user1)
    session.add(storage)
    session.commit()
    storage_in_db = session.query(Storage).filter_by(id=storage.id).first()
    assert storage_in_db is not None
    assert storage_in_db.id is not None
    assert storage_in_db.description is not None
    assert user1 in storage_in_db.users
    assert len(storage_in_db.users) == 1
    assert user1.id == storage_in_db.users[0].id
    



def test_user_storages_recorded_in_DB():
        """
        Test if users storages recorded in DB.
        Test if two users can be in the same storage.
        """
        user1 = user_for_tests()
        user2 = user_for_tests(email='my@mail.ru')
        storage1 = storage_for_tests(users=[user1, user2])
        storage2 = storage_for_tests(users=[user1, user2])
        session.add_all([user1, user2, storage1, storage2])
        session.commit()
        storage1_from_db = session.query(Storage).filter_by(id=storage1.id).first()
        storage2_from_db = session.query(Storage).filter_by(id=storage2.id).first()
        assert storage1_from_db.users is not None
        assert storage2_from_db.users is not None
        assert len(storage1_from_db.users) == 2
        assert len(storage2_from_db.users) == 2
        assert user1 in storage1_from_db.users
        assert user2 in storage1_from_db.users
        assert user1 in storage2_from_db.users
        assert user2 in storage2_from_db.users


def test_user_have_two_storages_recorded_in_DB():
        """
        Test if users storages recorded in DB.
        Test if two storages can be in the same user.
        """
        user1 = user_for_tests()
        user2 = user_for_tests()
        storage1 = storage_for_tests(users=[user1, user2])
        storage2 = storage_for_tests(users=[user1, user2])
        session.add_all([user1, user2, storage1, storage2])
        session.commit()
        user1_from_db = session.query(User).filter_by(id=user1.id).first()
        assert len(user1_from_db.storages) == 2
        assert storage1 in user1_from_db.storages
        assert storage2 in user1_from_db.storages


