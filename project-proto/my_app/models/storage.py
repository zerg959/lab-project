# my_app/models/storage.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models import db

class Storage(db.Model):
    __tablename__ = "storage"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255))
    zones = Column(JSON)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref="storages")

    def __repr__(self):
        return f"<Storage {self.name}>"

    def add_zone(self, zone_name, control_params):
       if not self.zones:
          self.zones = {}
       self.zones[zone_name] = control_params