# routes/dht22_routes.py
from flask import Blueprint, jsonify, current_app
import json

dht22_bp = Blueprint('dht22', __name__, url_prefix='/dht22')
DHT22_TEST_DATA_FILE = "sensors_test_data/dht22_test_data.json"
@dht22_bp.route('/data')
def get_sensor_data():
    try:
        # Open and load data from json.
        with open(DHT22_TEST_DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)  # Return data as JSON.
    except FileNotFoundError:
        current_app.logger.error(
            f"File not found: {DHT22_TEST_DATA_FILE}"
            )
        return jsonify({"error": "Test data file not found"}), 500
    except json.JSONDecodeError:
        current_app.logger.error(
            f"Invalid JSON in file: {DHT22_TEST_DATA_FILE}"
            )
        return jsonify({"error": "Invalid JSON format in test data file"}), 500
