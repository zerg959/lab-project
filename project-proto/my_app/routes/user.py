# my_app/routes/user.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Storage, Gadget, Zone, Param
from services.gadget_service import GadgetService
from functools import wraps
user_bp = Blueprint('user', __name__)

gadget_service = GadgetService()

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
         if not current_user.role == 'admin':
             return render_template('error.html', error="Admin role required")
         return func(*args, **kwargs)
    return decorated_function

@user_bp.route('/dashboard')
@login_required
def dashboard():
   if current_user.role == 'admin':
          storages = Storage.query.all()
   else:
       storages = Storage.query.filter_by(user_id=current_user.id).all()
   return render_template('user/dashboard.html', storages = storages)
# —писок хранилищ пользовател€
@user_bp.route('/storages')
@login_required
def list_storages():
   if current_user.role == 'admin':
       storages = Storage.query.all()
   else:
       storages = Storage.query.filter_by(user_id=current_user.id).all()
   return render_template('user/list_storages.html', storages=storages)

# ƒобавление хранилища пользователем
@user_bp.route('/storages/add', methods=['GET', 'POST'])
@login_required
def add_storage():
    if request.method == 'POST':
       name = request.form['name']
       description = request.form['description']
       storage = Storage(name=name, description=description, user_id=current_user.id)
       db.session.add(storage)
       db.session.commit()
       return redirect(url_for('user.list_storages'))
    return render_template('user/add_storage.html')

# –едактирование хранилища пользователем
@user_bp.route('/storages/edit/<int:storage_id>', methods=['GET', 'POST'])
@login_required
def edit_storage(storage_id):
    storage = Storage.query.get_or_404(storage_id)
    if current_user.role != 'admin' and storage.user_id != current_user.id:
         return render_template('error.html', error="Permission denied!")
    if request.method == 'POST':
       storage.name = request.form['name']
       storage.description = request.form['description']
       db.session.commit()
       return redirect(url_for('user.list_storages'))
    return render_template('user/edit_storage.html', storage=storage)

# ”даление хранилища пользователем
@user_bp.route('/storages/delete/<int:storage_id>', methods=['GET'])
@login_required
def delete_storage(storage_id):
    storage = Storage.query.get_or_404(storage_id)
    if current_user.role != 'admin' and storage.user_id != current_user.id:
        return render_template('error.html', error="Permission denied!")
    db.session.delete(storage)
    db.session.commit()
    return redirect(url_for('user.list_storages'))


# ƒобавление зоны в хранилище пользователем
@user_bp.route('/storages/<int:storage_id>/zones/add', methods=['GET', 'POST'])
@login_required
def add_zone(storage_id):
    storage = Storage.query.get_or_404(storage_id)
    if current_user.role != 'admin' and storage.user_id != current_user.id:
        return render_template('error.html', error="Permission denied!")
    if request.method == 'POST':
        zone_name = request.form['zone_name']
        min_temp = request.form.get('min_temp')
        max_temp = request.form.get('max_temp')
        min_humidity = request.form.get('min_humidity')
        max_humidity = request.form.get('max_humidity')
        control_params = {}
        if min_temp:
            control_params['min_temp'] = min_temp
        if max_temp:
            control_params['max_temp'] = max_temp
        if min_humidity:
            control_params['min_humidity'] = min_humidity
        if max_humidity:
            control_params['max_humidity'] = max_humidity
        storage.add_zone(zone_name,control_params)
        db.session.commit()
        return redirect(url_for('user.list_storages'))
    return render_template('user/add_zone.html', storage=storage)
# ”даление зоны из хранилища пользователем
@user_bp.route('/storages/<int:storage_id>/zones/delete/<zone_name>', methods=['GET'])
@login_required
def delete_zone(storage_id, zone_name):
    storage = Storage.query.get_or_404(storage_id)
    if current_user.role != 'admin' and storage.user_id != current_user.id:
          return render_template('error.html', error="Permission denied!")
    if storage and storage.zones and zone_name in storage.zones:
         del storage.zones[zone_name]
         db.session.commit()
    return redirect(url_for('user.list_storages'))

@user_bp.route('/zone/<int:zone_id>')
@login_required
def zone_page(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    gadgets = Gadget.query.filter_by(zone_id=zone_id).all()
    storage = Storage.query.filter(Storage.id == zone.storage_id).first()
    return render_template('user/zone_page.html', storage = storage, zone = zone, gadgets = gadgets )
# gadget routes

@user_bp.route('/gadget/manual_start/<int:gadget_id>')
@login_required
def manual_start(gadget_id):
    gadget = Gadget.query.get_or_404(gadget_id)
    gadget_service.set_gadget_manual(gadget, manual_status=True)
    return redirect(url_for('user.zone_page', zone_id=gadget.zone_id))

@user_bp.route('/gadget/manual_stop/<int:gadget_id>')
@login_required
def manual_stop(gadget_id):
    gadget = Gadget.query.get_or_404(gadget_id)
    gadget_service.set_gadget_manual(gadget, manual_status=False)
    return redirect(url_for('user.zone_page', zone_id=gadget.zone_id))

@user_bp.route('/gadget/set_interval/<int:gadget_id>', methods = ['POST'])
@login_required
def set_interval(gadget_id):
    interval = request.form.get('interval')
    gadget = Gadget.query.get_or_404(gadget_id)
    gadget_service.set_gadget_interval(gadget, interval)
    return redirect(url_for('user.zone_page', zone_id=gadget.zone_id))