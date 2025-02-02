from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, Table)
from .users import User

Base = declarative_base()

# association_table = Table(
#     'storage_users', Base.metadata,
#     Column('storage_id', ForeignKey('storages.id'), primary_key=True),
#     Column('user_id', ForeignKey('users.id'), primary_key=True)
# )


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
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    description = Column(String, nullable=True)
    user = relationship("User", backref='storages')

    # users = relationship("User",
    #                      secondary=association_table,
    #                      back_populates='storages')