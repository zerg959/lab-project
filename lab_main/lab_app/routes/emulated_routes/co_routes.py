# routes/co_routes.py
from flask import Blueprint, jsonify, current_app
import json

co_bp = Blueprint('co', __name__, url_prefix='/co')
CO_TEST_DATA_FILE = "sensors_test_data/co_test_data.json"
@co_bp.route('/data')
def co_sensor_data():
    # breakpoint()
    try:
        # Open and load data from json.
        with open(CO_TEST_DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)  # Return the data as JSON
    except FileNotFoundError:
        current_app.logger.error(
            f"File not found: {CO_TEST_DATA_FILE}"
            )
        return jsonify({"error": "Test data file not found"}), 500
    except json.JSONDecodeError:
        current_app.logger.error(f"Invalid JSON in file: {CO_TEST_DATA_FILE}")
        return jsonify(
            {"error": "Invalid JSON format in test data file"}
            ), 500
