pip install -r requirements.txt

python my_app/app.py
 
python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade