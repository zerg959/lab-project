# my_app/models/param.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from models import db

class Param(db.Model):
    __tablename__ = "param"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    # param_max = Column(Float)
    # param_min = Column(Float)
    param_curr = Column(Float)
    gadget_id = Column(Integer, ForeignKey('gadget.id'))
    gadget = relationship("Gadget", backref="params")
    param_data = Column(JSON)

    def __repr__(self):
         return f'<Param {self.description}>'