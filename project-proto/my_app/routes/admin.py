# my_app/routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Storage, User
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.role == 'admin' and not current_user.is_super_user():
            return render_template('error.html', error="Admin role required")
        return func(*args, **kwargs)
    return decorated_function
def superuser_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
         if not current_user.is_super_user():
             return render_template('error.html', error="Superuser role required")
         return func(*args, **kwargs)
    return decorated_function

# Список хранилищ
@admin_bp.route('/storages')
@login_required
@admin_required
def list_storages():
   storages = Storage.query.all()
   return render_template('admin/list_storages.html', storages=storages)
# Добавление хранилища
@admin_bp.route('/storages/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_storage():
  if request.method == 'POST':
      name = request.form['name']
      description = request.form['description']
      storage = Storage(name=name, description=description, user_id=current_user.id)
      db.session.add(storage)
      db.session.commit()
      return redirect(url_for('admin.list_storages'))
  return render_template('admin/add_storage.html')
# Редактирование хранилища
@admin_bp.route('/storages/edit/<int:storage_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_storage(storage_id):
    storage = Storage.query.get_or_404(storage_id)
    if request.method == 'POST':
       storage.name = request.form['name']
       storage.description = request.form['description']
       db.session.commit()
       return redirect(url_for('admin.list_storages'))
    return render_template('admin/edit_storage.html', storage=storage)
# Удаление хранилища
@admin_bp.route('/storages/delete/<int:storage_id>', methods=['GET'])
@login_required
@admin_required
def delete_storage(storage_id):
   storage = Storage.query.get_or_404(storage_id)
   db.session.delete(storage)
   db.session.commit()
   return redirect(url_for('admin.list_storages'))
# Добавление зоны в хранилище администратором
@admin_bp.route('/storages/<int:storage_id>/zones/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_zone(storage_id):
    storage = Storage.query.get_or_404(storage_id)
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
       return redirect(url_for('admin.list_storages'))
    return render_template('admin/add_zone.html', storage=storage)
# Удаление зоны из хранилища администратором
@admin_bp.route('/storages/<int:storage_id>/zones/delete/<zone_name>', methods=['GET'])
@login_required
@admin_required
def delete_zone(storage_id, zone_name):
    storage = Storage.query.get_or_404(storage_id)
    if storage and storage.zones and zone_name in storage.zones:
       del storage.zones[zone_name]
       db.session.commit()
    return redirect(url_for('admin.list_storages'))

# Список пользователей
@admin_bp.route('/users')
@login_required
@superuser_required
def list_users():
  users = User.query.all()
  return render_template('admin/list_users.html', users=users)

# Раздача прав
@admin_bp.route('/users/change/<int:user_id>/<role>', methods=['GET'])
@login_required
@superuser_required
def change_user_role(user_id, role):
    user = User.query.get_or_404(user_id)
    if role == 'admin' or role == 'user':
        user.role = role
        db.session.commit()
    return redirect(url_for('admin.list_users'))
# Удаление администратора
@admin_bp.route('/users/delete/<int:user_id>', methods=['GET'])
@login_required
@superuser_required
def delete_user(user_id):
   user = User.query.get_or_404(user_id)
   if not user.is_super_user():
       db.session.delete(user)
       db.session.commit()
       # Если нет ни одного админа, то суперюзер становится админом
       admin_count = User.query.filter_by(role='admin').count()
       if admin_count == 0:
         current_user.role = 'admin'
         db.session.commit()
   return redirect(url_for('admin.list_users'))