from run_lab import create_app
from lab_db import reset_db
app = create_app()
if __name__ == "__main__":
    with app.app_context():
        reset_db(app)
        print("Database has been reset.")
