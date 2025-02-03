from sqlalchemy.orm import validates, relationship
from sqlalchemy import (Column, Integer, String, CheckConstraint)
from .base import Base
from .associations import association_table


USER_ROLE_USER = 'user'
"""Constant for user role"""
USER_ROLE_ADMIN = 'admin'
"""Constant for admin role"""


class User(Base):
    """
    User model for DB-table 'users'
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    """
    Unique primary key user-ID, integer.
    """
    name = Column(String, nullable=False)
    """
    User name: non-unique, string.
    """
    email = Column(String, nullable=False, unique=True, index=True)
    """
    Email: unique, string, email format.
    """
    role = Column(String,
                  CheckConstraint(f'role IN \
                                  ("{USER_ROLE_USER}", "{USER_ROLE_ADMIN}")'
                                  ),
                  nullable=False,
                  default=USER_ROLE_USER
                  )
    # storages = relationship("Storage", backref='user')
    """
    User role.
    Only allowed role names are allowed ('user', 'admin')
    """
    storages = relationship("Storage",
                            secondary=association_table,
                            back_populates="users")
    """
    List of storages user can manage.
    """

    @validates('role')
    def role_validtion(self, key, value):
        """
        Validation role value function.
        Checks if the role in allowed values.
        :param key: field name (always 'role).
        :param value: field value.
        :raises ValueError: If value not allowed.
        :return: Role value.
        """
        if value is None:
            value = USER_ROLE_USER
        if value not in [USER_ROLE_ADMIN, USER_ROLE_USER]:
            raise ValueError(f"Incorrect role {value}. Use {USER_ROLE_USER} \
                              or {USER_ROLE_ADMIN}.")
        return value
