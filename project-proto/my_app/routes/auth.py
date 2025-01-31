# my_app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import db, User
from werkzeug.security import check_password_hash
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
          login_user(user)
          return redirect(url_for('user.dashboard'))
        return render_template('auth/login.html', error="Invalid credentials")
     return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
   if request.method == 'POST':
     username = request.form['username']
     password = request.form['password']
     user = User(username=username)
     user.set_password(password)
     db.session.add(user)
     db.session.commit()
     return redirect(url_for('auth.login'))
   return render_template('auth/register.html')
@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))