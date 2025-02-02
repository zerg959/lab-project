from sqlalchemy.orm import declarative_base
from sqlalchemy import (Column, Integer, String, 
                        ForeignKey, Boolean, REAL, CheckConstraint)
Base = declarative_base()

USER_ROLE_USER = 'user'
USER_ROLE_ADMIN = 'admin'


class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String,
                  CheckConstraint(f'role IN \
                                  ("{USER_ROLE_USER}", "{USER_ROLE_ADMIN}")'
                                  ),
                  nullable=False,
                  default=USER_ROLE_USER
                  )
