from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar variables de entorno desde .env
    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Solo configurar la base de datos si USE_DB está configurado
    if os.getenv('USE_DB') == 'True':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app