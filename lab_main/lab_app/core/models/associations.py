from sqlalchemy import Table, Column, ForeignKey
from .base import metadata

association_table = Table(
    "storage_users",
    metadata,
    Column("storage_id", ForeignKey("storages.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)
"""
Association table for Storage and User models:
helps to organize Many-to-Many realtionships.
"""
