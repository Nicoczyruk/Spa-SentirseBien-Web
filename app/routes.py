from flask import Blueprint, render_template, request, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
import pyodbc
from werkzeug.security import check_password_hash, generate_password_hash
from . import odbc_connection_string
from app import app, engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import text

main = Blueprint('main', __name__)
# Configurar logging para debugging
logging.basicConfig(level=logging.DEBUG)

class User(UserMixin):
    def __init__(self, id, nombre_usuario, email, rol):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.rol = rol

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

login_manager = LoginManager()
login_manager.init_app(app)  # Asegúrate de que esto se haga en la creación de la aplicación

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario, email, rol FROM usuarios WHERE id_usuario = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return User(id=user[0], nombre_usuario=user[1], email=user[2], rol=user[3])
    return None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gallery') 
def gallery():

    images1 = [
        'testimonials-1.jpg',
        'testimonials-2.jpg',
        'testimonials-3.jpg',
    ]

    return render_template('gallery.html', images = images1)

@main.route('/about')
def about():

    return render_template('about.html')

@main.route('/services')
def services():
    services_data = {
        'Masajes': [
            {'image': 'antiStress.jpg', 'name': 'Anti-stress', 'description': 'Descripción del servicio...', 'price': '$40'},
            {'image': 'masajeDescontracturante.jpg', 'name': 'Descontracturantes', 'description': 'Descripción del servicio...', 'price': '$50'},
            {'image': 'masajeConPiedrasCalientes.jpg', 'name': 'Masajes con piedras calientes', 'description': 'Descripción del servicio...', 'price': '$60'},
            {'image': 'masajeCirculatorio.jpg', 'name': 'Circulatorios', 'description': 'Descripción del servicio...', 'price': '$55'}
        ],
        'Belleza': [
            {'image': 'liftingPesta.jpg', 'name': 'Lifting de pestaña', 'description': 'Descripción del servicio...', 'price': '$70'},
            {'image': 'depilacionFacial.jpg', 'name': 'Depilación facial', 'description': 'Descripción del servicio...', 'price': '$30'},
            {'image': 'bellezaManosYPies.jpg', 'name': 'Belleza de manos y pies', 'description': 'Descripción del servicio...', 'price': '$45'}
        ],
        'Tratamientos Faciales': [
            {'image': 'puntaDiamante.jpg', 'name': 'Punta de Diamante', 'description': 'Descripción del servicio...', 'price': '$80'},
            {'image': 'limpiezaHidratacion.jpg', 'name': 'Limpieza profunda + Hidratación', 'description': 'Descripción del servicio...', 'price': '$90'},
            {'image': 'crioFrecuencia.jpg', 'name': 'Crio frecuencia facial', 'description': 'Descripción del servicio...', 'price': '$100'}
        ],
        'Tratamientos Corporales': [
            {'image': 'velaSlim.jpg', 'name': 'VelaSlim', 'description': 'Descripción del servicio...', 'price': '$120'},
            {'image': 'dermoHealth.jpg', 'name': 'DermoHealth', 'description': 'Descripción del servicio...', 'price': '$110'},
            {'image': 'crioFrecuenciaCorporal.jpg', 'name': 'Criofrecuencia', 'description': 'Descripción del servicio...', 'price': '$115'},
            {'image': 'ultraCavitacion.jpg', 'name': 'Ultracavitación', 'description': 'Descripción del servicio...', 'price': '$105'}
        ]
    }

    return render_template('services.html', categories=services_data)

@main.route('/news')
def news():
    return render_template('news.html', title = 'Noticias')

@main.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/sql-test', methods=['GET', 'POST'])
def sql_test():
    usuarios = []
    try:
        with engine.connect() as connection:
            if request.method == 'POST':
                # Crear usuario
                if 'create_user' in request.form:
                    nombre_usuario = request.form.get('nombre_usuario')
                    password = request.form.get('password')
                    email = request.form.get('email')
                    if nombre_usuario and password and email:
                        connection.execute(
                            text("INSERT INTO usuarios (nombre_usuario, password, email) VALUES (:nombre_usuario, :password, :email)"),
                            {"nombre_usuario": nombre_usuario, "password": password, "email": email}
                        )
                        connection.commit()
                        flash('Usuario creado exitosamente', 'success')
                    else:
                        flash('Todos los campos son obligatorios', 'danger')

                # Modificar usuario
                elif 'modify_user' in request.form:
                    id_usuario = request.form.get('id_usuario')
                    new_nombre_usuario = request.form.get('new_nombre_usuario')
                    new_email = request.form.get('new_email')
                    connection.execute(
                        text("UPDATE usuarios SET nombre_usuario = :new_nombre_usuario, email = :new_email WHERE id_usuario = :id_usuario"),
                        {"new_nombre_usuario": new_nombre_usuario, "new_email": new_email, "id_usuario": id_usuario}
                    )
                    connection.commit()
                    flash('Usuario modificado exitosamente', 'success')

                # Eliminar usuario
                elif 'delete_user' in request.form:
                    id_usuario = request.form.get('id_usuario')
                    connection.execute(
                        text("DELETE FROM usuarios WHERE id_usuario = :id_usuario"),
                        {"id_usuario": id_usuario}
                    )
                    connection.commit()
                    flash('Usuario eliminado exitosamente', 'success')
            # Si no hay POST o no se hizo 'load_users', cargar usuarios por defecto
            if not usuarios:
                result = connection.execute(text("SELECT * FROM usuarios"))
                usuarios = result.fetchall()

        return render_template('sql_test.html', title='SQL Test', usuarios=usuarios)

    except SQLAlchemyError as e:
        logging.error(f"Error al ejecutar la consulta SQL: {e}")
        flash(f"Ocurrió un error al ejecutar la consulta: {str(e)}", 'danger')
        return redirect(url_for('sql_test'))

    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        flash(f"Ocurrió un error inesperado: {str(e)}", 'danger')
        return redirect(url_for('sql_test'))

def get_db_connection():
    conn = pyodbc.connect(odbc_connection_string)
    return conn

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario, email, password, rol FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        user_obj = User(id=user[0], nombre_usuario=user[1], email=user[2], rol=user[4])
        login_user(user_obj)  # Esto debería guardar el user_id en la sesión

        session.permanent = True  # Asegura que la sesión sea permanente

        print(f"User logged in with ID: {user_obj.get_id()}")
        print(f"Session contents: {session.items()}")

        return jsonify({'success': True, 'message': 'Login successful', 'username': user[1]})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    
@app.route('/check_session', methods=['GET'])
def check_session():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'username': current_user.nombre_usuario})
    else:
        return jsonify({'logged_in': False})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Elimina la sesión del usuario
    session.clear()  # Limpia toda la información de la sesión
    return jsonify({'success': True})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserta el nuevo cliente
        cursor.execute("""
            INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
            VALUES (?, ?, ?, ?, ?);
        """, (data['nombre'], data['apellido'], data['email'], data['telefono'], data['direccion']))
        
        conn.commit()

        # Obtener el ID del cliente recién insertado usando el email
        cursor.execute("SELECT id_cliente FROM clientes WHERE email = ?", data['email'])
        id_cliente = cursor.fetchone()[0]

        # Hashear la contraseña
        hashed_password = generate_password_hash(data['password'])

        # Crear el usuario vinculado al cliente con el rol de "Cliente"
        cursor.execute("""
            INSERT INTO usuarios (id_cliente, nombre_usuario, password, email, rol)
            VALUES (?, ?, ?, ?, ?);
        """, (id_cliente, data['nombre_usuario'], hashed_password, data['email'], 'Cliente'))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/perfil')
@login_required  # Asegura que el usuario esté logueado
def perfil():
    user_id = current_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)", (user_id,))
    client_data = cursor.fetchone()
    conn.close()

    if client_data:
        return render_template('perfil.html', client=client_data)
    else:
        return "No se encontraron datos del cliente", 404
    
from flask import redirect, url_for, flash

@app.route('/consulta', methods=['GET', 'POST'])
@login_required  # Asegura que el usuario esté logueado
def consulta():
    if request.method == 'POST':
        nombre = request.form['nombre']  # El nombre se extrae del formulario
        email = request.form['email']
        titulo = request.form['titulo']
        mensaje = request.form['mensaje']

        # Guardar la consulta en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultas (nombre, email, tituloConsulta, mensaje) VALUES (?, ?, ?, ?)", 
                       (nombre, email, titulo, mensaje))
        conn.commit()
        conn.close()

        # Redirigir a la página de consulta con un mensaje de éxito
        return redirect(url_for('consulta', success=True))
    
    return render_template('consulta.html', success=request.args.get('success'))



@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.rol != 'Administrador':
        return redirect(url_for('main.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Monitoreo - Contar cantidad de clientes
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'Cliente'")
    total_clients = cursor.fetchone()[0]

    # Obtener lista de empleados
    cursor.execute("SELECT nombre_usuario, email FROM usuarios WHERE rol = 'Empleado'")
    employees = cursor.fetchall()

    conn.close()

    return render_template('admin_dashboard.html', total_clients=total_clients, employees=employees)

@app.route('/create_employee', methods=['POST'])
@login_required
def create_employee():
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'message': 'No autorizado'})

    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    email = f'{username}@spasentirsebien.com'  # Generar un email único basado en el nombre de usuario

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, email, password, rol) VALUES (?, ?, ?, 'Empleado')",
                       (username, email, password))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/empleado_dashboard')
@login_required
def empleado_dashboard():
    if current_user.rol not in ['Empleado', 'Administrador']:
        return redirect(url_for('main.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener las consultas de los clientes (haciendo un JOIN con clientes para obtener el nombre y apellido)
    cursor.execute("""
    SELECT q.id_consulta, c.nombre, c.apellido, q.email, q.tituloConsulta, q.mensaje, q.fecha
    FROM consultas q
    LEFT JOIN clientes c ON q.email = c.email
    ORDER BY q.fecha DESC
    """)
    consultas = cursor.fetchall()

    # Obtener los mensajes de empleo (filtrando por "CV" en el título)
    cursor.execute("""
        SELECT c.nombre, c.apellido, q.email, q.tituloConsulta, q.mensaje, q.fecha
        FROM consultas q
        LEFT JOIN clientes c ON q.email = c.email
        WHERE q.tituloConsulta LIKE '%CV%'
        ORDER BY q.fecha DESC
    """)
    empleos = cursor.fetchall()

    conn.close()

    return render_template('empleado_dashboard.html', consultas=consultas, empleos=empleos)

@app.route('/responder_consulta', methods=['POST'])
@login_required
def responder_consulta():
    try:
        consulta_id = request.form.get('consultaId')
        print(consulta_id)
        respuesta = request.form.get('respuesta')

        if not consulta_id or not respuesta:
            return jsonify({'success': False, 'message': 'Datos incompletos'})

        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar la consulta de la base de datos después de responder
        cursor.execute("DELETE FROM consultas WHERE id_consulta = ?", (consulta_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al responder consulta: {str(e)}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500
