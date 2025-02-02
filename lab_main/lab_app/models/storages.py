from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, UniqueConstraint)

Base = declarative_base()


def _generate_storage_description():
    return "Storage №"


class Storage(Base):
    """
    Storage model:
    to create Storage with Zones.
    One Storage can be managed by multiply Users.
    """
    __tablename__ = 'storages'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),
                     nullable=False, index=True)
    description = Column(String, nullable=True,
                         default=_generate_storage_description)
    user = relationship("User", backref='storages')
    __table_args__ = (
        UniqueConstraint('user.id'),
    )
