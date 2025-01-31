# my_app/models/gadget.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from models import db
import enum
import time
import requests

class GadgetType(enum.Enum):
    sensor = 'sensor'
    regulator = 'regulator'

class Gadget(db.Model):
    __tablename__ = "gadget"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    type = Column(Enum(GadgetType))
    status = Column(String(20), default='off')
    zone_id = Column(Integer, ForeignKey('zone.id'))
    zone = relationship("Zone", backref="gadgets")
    is_manual = Column(Boolean(), default=False) # Флаг для ручного управления
    interval = Column(Integer, default=0) # Интервал для работы в сек.
    esp32_url = Column(String(255))
    def __repr__(self):
       return f'<Gadget {self.description}>'

    def manual_start(self):
        if not self.is_manual:
            self.is_manual = True
            self.status = "on"
            self.send_command_to_esp32({'status': 'on'})
            db.session.commit()

    def manual_stop(self):
         if self.is_manual:
            self.is_manual = False
            self.status = "off"
            self.send_command_to_esp32({'status': 'off'})
            db.session.commit()

    def set_interval(self, interval):
         self.interval = interval
         db.session.commit()
    def send_command_to_esp32(self, data):
        if self.esp32_url:
         try:
            response = requests.post(self.esp32_url, json=data)
            response.raise_for_status()
            print("Command sent successfully")
         except requests.exceptions.RequestException as e:
             print(f"Error sending command: {e}")

class Sensor(Gadget):
    __tablename__ = "sensor"
    id = Column(Integer, ForeignKey("gadget.id"), primary_key=True)
    last_check = Column(Integer, default=0)
    __mapper_args__ = {
        'polymorphic_identity':'sensor',
    }

    def __repr__(self):
        return f'<Sensor {self.description}>'

    def check_sensor(self, params):
       if time.time() - self.last_check >= self.interval:
         # some code to get data
         value = time.time()
         self.last_check = time.time()
         # save to param object
         for param in params:
             param.param_curr = value # value or some data from sensor
         # send data to flask
         self.send_data_to_flask({"gadget_id":self.id, "temperature": value, "time":time.time()})
         db.session.commit()
    def send_data_to_flask(self, data):
       if self.esp32_url:
         try:
             response = requests.post(self.esp32_url.replace("/control","/sensor_data"), json=data) # change url to sensor
             response.raise_for_status()
             print("Data sent successfully")
         except requests.exceptions.RequestException as e:
             print(f"Error sending command: {e}")


class Regulator(Gadget):
    __tablename__ = "regulator"
    id = Column(Integer, ForeignKey("gadget.id"), primary_key=True)
    last_change = Column(Integer, default=0)
    __mapper_args__ = {
      'polymorphic_identity':'regulator'
    }
    def __repr__(self):
        return f'<Regulator {self.description}>'
    def regulate(self):
      if time.time() - self.last_change >= self.interval:
          if self.status == 'off':
            self.status = 'on'
            self.send_command_to_esp32({'status':'on'})
          elif self.status == 'on':
            self.status = 'off'
            self.send_command_to_esp32({'status':'off'})
          self.last_change = time.time()
          db.session.commit()