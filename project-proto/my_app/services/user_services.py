# my_app/services/user_service.py
from models import db, User

class UserService:
   def create_user(self, username, password, role='user'):
      user = User(username=username, role=role)
      user.set_password(password)
      db.session.add(user)
      db.session.commit()
      return user
   def set_user_role(self, user, role):
      user.role = role
      db.session.commit()
   def delete_user(self, user):
       db.session.delete(user)
       db.session.commit()