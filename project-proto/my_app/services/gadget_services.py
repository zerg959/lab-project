# my_app/services/gadget_service.py
from models import db, Gadget, Sensor, Regulator, Param

class GadgetService:
   def create_gadget(self, description, type, zone_id, esp32_url, check_period=None, work_period=None):
       if type == 'sensor':
           gadget = Sensor(description=description, type=type, zone_id=zone_id, esp32_url=esp32_url, check_period = check_period)
       elif type == 'regulator':
            gadget = Regulator(description=description, type=type, zone_id=zone_id, esp32_url=esp32_url, work_period = work_period)
       else:
            gadget = Gadget(description=description, type=type, zone_id=zone_id, esp32_url=esp32_url)
       db.session.add(gadget)
       db.session.commit()
       return gadget
   def remove_gadget(self, gadget):
      db.session.delete(gadget)
      db.session.commit()
   def set_gadget_manual(self, gadget, manual_status):
       if manual_status:
           gadget.manual_start()
       else:
           gadget.manual_stop()
   def set_gadget_interval(self, gadget, interval):
      gadget.set_interval(interval)
   def get_gadgets_by_zone(self, zone_id):
       return Gadget.query.filter_by(zone_id=zone_id).all()
   def check_sensors(self, zone_id):
       gadgets = Gadget.query.filter_by(zone_id=zone_id).all()
       for gadget in gadgets:
         if gadget.type.value == 'sensor':
            params = Param.query.filter_by(gadget_id=gadget.id).all()
            if params:
              gadget.check_sensor(params)
   def regulate_regulators(self, zone_id):
      gadgets = Gadget.query.filter_by(zone_id=zone_id).all()
      for gadget in gadgets:
         if gadget.type.value == 'regulator':
            gadget.regulate()