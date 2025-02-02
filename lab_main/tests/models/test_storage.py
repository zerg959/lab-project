from lab_main.lab_app.models.users import User, Base
from . objs_for_test import user_for_tests, db_for_tests


def test_storage_created():
    """
    Test if storage created in DB with params.
    """
    storage