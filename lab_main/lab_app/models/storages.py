from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String,)
from .associations import association_table
from .base import Base


class Storage(Base):
    """
    Storage model:
    to create Storage with Zones.
    One Storage can be managed by multiply Users.
    Attributes:
    id (int): Unique storage ID.
    description (str): Storage description.
    users (list): Linked users.
    """
    __tablename__ = 'storages'
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=True)
    # user = relationship("User", backref='storages')
    # user_id = Column(Integer, ForeignKey('users.id'),
    #  nullable=False, index=True)
    users = relationship("User",
                         secondary=association_table,
                         back_populates='storages')
