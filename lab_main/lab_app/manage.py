from run_lab import app
from lab_db import reset_db

if __name__ == "__main__":
    with app.app_context():
        reset_db(app)
        print("Database has been reset.")
