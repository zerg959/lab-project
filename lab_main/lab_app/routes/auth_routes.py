from flask import (
  Blueprint, render_templates, redirect,
  url_for, request
  )
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
          email = request.form['email']
          password = request.form['password']

          existing_user = User.query.filter_by(email=email).first()
          if existing_user:
               return render_templates('register.html', error='Email already exists')