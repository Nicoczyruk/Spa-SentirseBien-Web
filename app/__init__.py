from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import urllib
import sqlalchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar variables de entorno desde .env
    load_dotenv()

    # Construir la cadena de conexión
    connection_string = os.getenv('SQLALCHEMY_DATABASE_URI')
    odbc_connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"Server=tcp:spa-sentirse-bien-server.database.windows.net,1433;"
        f"Database=SpaSentirseBienBD;"
        f"Uid={os.getenv('DB_USER')};"
        f"Pwd={os.getenv('DB_PASSWORD')};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )

    connection_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_connection_string)}"

    app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app