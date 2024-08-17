from app import create_app, db
import os

app = create_app()

if os.getenv('USE_DB') == 'True':
    with app.app_context():
        db.create_all()  # Esto crea todas las tablas en la base de datos

if __name__ == "__main__":
    app.run(debug=True)