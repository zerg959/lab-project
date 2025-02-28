from flask import Flask
import os
import logging
from lab_db import init_app, lab_db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    app.root_path, 'database.db'
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.INFO)
lab_db.init_app(app)


@app.route("/")
def home():
    return "hi"


if __name__ == "__main__":
    # init_app(app)  # DB Init
    app.run(debug=True)
