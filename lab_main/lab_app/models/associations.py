from sqlalchemy import Table, Column, ForeignKey
from .base import Base

association_table = Table(
    'storage_users', Base.metadata,
    Column('storage_id', ForeignKey('storages.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)