from sqlalchemy.orm import sessionmaker
from models import User, Base


class StorageService(Base):
    __tablename__='storage_service'
    