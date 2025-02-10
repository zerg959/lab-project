from sqlalchemy import text


def test_db_connection(engine):
    """
    Test if the database connection works.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar()
        assert result == 1
