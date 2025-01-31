# my_app/app.py
from flask import Flask, render_template
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.api import api_bp
from routes.user import user_bp
from routes.admin import admin_bp
from models import db, User, Zone
from services.gadget_service import GadgetService
from services.storage_service import StorageService
import time

app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = 'hub10.ru:5000'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')


# Маршрут для личного кабинета с поддоменом и динамическим URL
@app.route('/<storage_name>', subdomain="lab")
def storage_dashboard(storage_name):
   from models import Storage
   storage = Storage.query.filter_by(name=storage_name).first()
   if not storage:
     return render_template("error.html", error="Storage not found!")
   return render_template("dashboard.html", data=storage.zones, storage=storage)


gadget_service = GadgetService()
def scheduled_tasks():
    with app.app_context():
        while True:
            all_zones = Zone.query.all()
            for zone in all_zones:
               gadget_service.check_sensors(zone.id)
               gadget_service.regulate_regulators(zone.id)
            time.sleep(1) # run every 1 second

import threading
threading.Thread(target=scheduled_tasks).start()
if __name__ == '__main__':
   with app.app_context():
        db.create_all()
   app.run(debug=True, use_reloader = False)