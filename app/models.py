from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación uno a uno con Usuario
    usuario = db.relationship('Usuario', backref='cliente', uselist=False)

class Turno(db.Model):
    __tablename__ = 'turnos'
    id_turno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicios.id_servicio'), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default="Pendiente")

    # Índices para búsqueda rápida de turnos
    __table_args__ = (
        db.Index('idx_turno_cliente', 'id_cliente'),
        db.Index('idx_turno_servicio', 'id_servicio'),
    )

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id_servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en minutos
    precio = db.Column(db.Numeric(10, 2), nullable=False)

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), unique=True)
    nombre_usuario = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    rol = db.Column(db.String(50), nullable=False, default="Cliente")  # Ej. "Admin", "Empleado", "Cliente"

class Mensaje(db.Model):
    __tablename__ = 'mensajes'
    id_mensaje = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)  # Ej. "Consulta", "CV"
    titulo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Índice para facilitar la búsqueda por tipo de mensaje
    __table_args__ = (
        db.Index('idx_mensaje_tipo', 'tipo'),
    )