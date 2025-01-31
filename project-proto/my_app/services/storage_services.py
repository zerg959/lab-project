# my_app/services/storage_service.py
from models import db, Storage

class StorageService:
   def create_storage(self, name, description, user_id):
       storage = Storage(name=name, description=description, user_id=user_id)
       db.session.add(storage)
       db.session.commit()
       return storage

   def add_zone(self, storage, zone_name, control_params):
        storage.add_zone(zone_name, control_params)
        db.session.commit()
        return storage
   def remove_zone(self, storage, zone_name):
       if storage and storage.zones and zone_name in storage.zones:
           del storage.zones[zone_name]
           db.session.commit()
           return storage
       return None

   def get_storage_by_id(self, storage_id):
     return Storage.query.get(storage_id)

   def get_storages_by_user(self, user_id):
       return Storage.query.filter_by(user_id=user_id).all()

   def delete_storage(self, storage):
     db.session.delete(storage)
     db.session.commit()