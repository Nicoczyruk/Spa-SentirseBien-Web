import os
import urllib
from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# Configuración de la duración de la sesión
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Ajusta el tiempo que desees
app.config['SESSION_PERMANENT'] = True

# encriptacion de las cookies
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True  # Solo envía cookies a través de HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Evita el acceso a las cookies desde JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Evita CSRF en la mayoría de los casos

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