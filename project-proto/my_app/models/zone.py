# my_app/models/zone.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models import db

class Zone(db.Model):
   __tablename__ = "zone"
   id = Column(Integer, primary_key=True)
   name = Column(String(80), nullable=False)
   control_params = Column(JSON)
   storage_id = Column(Integer, ForeignKey('storage.id'))
   storage = relationship("Storage", backref="zones")

   def __repr__(self):
     return f'<Zone {self.name}>'