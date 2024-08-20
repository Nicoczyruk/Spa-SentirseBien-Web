import os
import urllib
from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Construir el string de conexión ODBC 18
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

# Crear la URL de conexión para SQLAlchemy
connection_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_connection_string)}"

# Configurar Flask y SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configurar el motor de SQLAlchemy
engine = create_engine(connection_url)

# Registrar las rutas
from .routes import main
app.register_blueprint(main)

# La aplicación ahora está lista para manejar las solicitudes
def create_app():
    return app