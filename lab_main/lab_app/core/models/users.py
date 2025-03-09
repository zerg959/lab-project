from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, CheckConstraint
from typing import List, Optional
from .base import Base
from .associations import association_table
from lab_db import lab_db
from flask_login import UserMixin


USER_ROLE_USER = "user"
"""Constant for user role"""
USER_ROLE_ADMIN = "admin"
"""Constant for admin role"""


class User(UserMixin, Base):
    """
    Represents a user in the system.

    Attributes:
      - id (int): Unique identifier for the user.
      - name (str): User's name. Must not be null.
      - email (str): User's email address. Must be unique and not null.
        Indexed for faster lookups.
      - role (str): User's role, which determines their permissions.
        Allowed values: :data:`USER_ROLE_USER` or :data:`USER_ROLE_ADMIN`.
        Enforced by a CHECK constraint in the database.
        Default is :data:`USER_ROLE_USER`.
      - storages (List):
        List of storages the user has access to.
        The relationship is many-to-many via the `association_table`.
    """

    __tablename__ = "users"
    id: Column[int] = Column(Integer, primary_key=True, nullable=False)
    name: Column[str] = Column(String, nullable=False)
    email: Column[str] = Column(
        String,
        nullable=False,
        unique=True,
        index=True)
    role: Column[str] = Column(
        String,
        CheckConstraint(
            f'role IN \
                                  ("{USER_ROLE_USER}", "{USER_ROLE_ADMIN}")'
        ),
        nullable=False,
        default=USER_ROLE_USER,
    )
    storages = relationship(
        "Storage", secondary=association_table, back_populates="users"
    )

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User id={self.id}: {self.name}"

    @validates("role")
    def role_validation(self, key: str, value: str) -> str:
        """
        Validates the user's role.

        Ensures that the role is one of the allowed values
        (:data:`USER_ROLE_USER` or :data:`USER_ROLE_ADMIN`).

        Args:
            key (str): The attribute being validated (always 'role').
            value (str): The proposed value for the role.

        Returns:
            str: The validated role value.

        Raises:
            ValueError: If the provided `value` is not a valid role.
        """
        if value is None:
            value = USER_ROLE_USER
        if value not in [USER_ROLE_ADMIN, USER_ROLE_USER]:
            raise ValueError(
                f"Incorrect role {value}. Use {USER_ROLE_USER} \
                              or {USER_ROLE_ADMIN}."
            )
        return value
