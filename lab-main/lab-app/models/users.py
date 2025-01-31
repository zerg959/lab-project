from sqlalchemy.orm import declarative_base
from sqlalchemy import (Column, Integer, String, 
                        ForeignKey, Boolean, REAL, CheckConstraint)
Base = declarative_base()


class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String,
                  CheckConstraint('role IN ("user", "admin")'),
                  nullable=False,
                  default='user'
                  )