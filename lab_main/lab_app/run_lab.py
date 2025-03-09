from flask import Flask, request
from flask_login import (
    LoginManager, login_requiered, current_user
    )
from flask_sqlalchemy import SQLAlchemy
import os, json
import logging
from dotenv import load_dotenv
# from emulator_config import setup_emulator
from lab_db import init_app, lab_db
from routes.emulated_routes import dht22_bp, co_bp
from core.models import Base, User

load_dotenv()
app = Flask(__name__)

# DB config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    app.root_path, 'database.db'
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_dev_secret')
app.logger.setLevel(logging.INFO)
lab_db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
# Set the login view function (name of the route)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Loading user


# Blueprints
app.register_blueprint(auth_bp)  # AuthBP
app.register_blueprint(dht22_bp)  # DHT22BP
app.register_blueprint(co_bp)  # CO2BP
# API_URL = setup_emulator(app, port=8001)  # test api url

# Protected routes
@app.route("/protected")
@login_requiered
def protected():
    return f"Logged in as: {current_user.email}"

# Routes
@app.route("/")
def home():
    return "hi"

# @app.route("/test_api")
# def test_api():
#     try:
#         # use API_URL
#         data = {"temperature": 25.0, "humidity": 60.0}
#         response = requests.post(API_URL, json=data)  # Use URL
#         response.raise_for_status()
#         return f"API test was successful. Response: {response.text}", 200
#     except requests.exceptions.RequestException as e:
#         return f"Error connecting to API: {e}", 500

# @app.before_first_request
# def create_tables():
#     Base.metadata.create_all(lab_db.engine)
#     app.logger.info("Creating tables")


# from core.models import Device, Parameter, Sensor, Storage, User, Zone


with app.app_context():  # DB Init
    lab_db.create_all()
    # Base.metadata.create_all(lab_db.engine)
    app.logger.info("Tables are creating.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
