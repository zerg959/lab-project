from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)
"""
Base class for all models of the app.
Need to organize same environment for objects.
"""
