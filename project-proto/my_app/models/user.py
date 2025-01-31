# my_app/models/user.py
 from flask_sqlalchemy import SQLAlchemy
 from sqlalchemy import Column, Integer, String
 from flask_login import UserMixin
 from werkzeug.security import generate_password_hash, check_password_hash

 db = SQLAlchemy()

 class User(db.Model, UserMixin):
     __tablename__ = "user"
     id = Column(Integer, primary_key=True)
     username = Column(String(80), unique=True, nullable=False)
     password_hash = Column(String(128))
     role = Column(String(20), default='user')

     def set_password(self, password):
        self.password_hash = generate_password_hash(password)

     def check_password(self, password):
        return check_password_hash(self.password_hash, password)

     def is_super_user(self):
        return self.username == 'superadmin'

     def __repr__(self):
          return f'<User {self.username}>'