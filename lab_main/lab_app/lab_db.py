from flask_sqlalchemy import SQLAlchemy
from flask import current_app


lab_db = SQLAlchemy()


def init_db(app):
    """
    Initialize SQLite DB.
    """
    lab_db.init_db(app)
    with app.app_context():
        lab_db.create_all()
        current_app.logger.info('Database initialized and tables created.')


def reset_db(app):
    """
    Drop DB (delete all tables and recreate new).
    """
    with app.app_context():
        lab_db.drop_all()
        lab_db.create_all()
        current_app.logger.info('Database reset.')
