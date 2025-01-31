# my_app/routes/api.py
from flask import Blueprint, request, jsonify
import requests
from models import Param, db, Gadget
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    gadget_id = data.get('gadget_id')
    temperature = data.get('temperature')
    timestamp = data.get('time')
    gadget = Gadget.query.get_or_404(gadget_id)
    if gadget.type.value == 'sensor':
       params = Param.query.filter_by(gadget_id=gadget.id).all()
       for param in params:
           param.param_curr = temperature
       db.session.commit()
    return jsonify({"message": "Data received"})

@api_bp.route('/regulators/<int:gadget_id>/control', methods=['POST'])
def control_regulator(gadget_id):
    data = request.get_json()
    status = data.get('status')
    gadget = Gadget.query.get_or_404(gadget_id)
    if gadget and gadget.esp32_url:
      try:
         response = requests.post(gadget.esp32_url, json={'status': status})
         response.raise_for_status()
         return jsonify({"message": "Command sent successfully"})
      except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error sending command: {e}"}), 500
    else:
        return jsonify({"error": f"Error sending command"}), 404