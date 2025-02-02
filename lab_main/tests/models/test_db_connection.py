from sqlalchemy import text
from . objs_for_test import db_for_tests


def test_db_connection():
    """
    Test if the database connection works.
    """
    db = db_for_tests()
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1
