from flask import Blueprint, render_template, request, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
import pyodbc
from werkzeug.security import check_password_hash, generate_password_hash
from . import odbc_connection_string
from app import app, engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import text
from datetime import datetime, timedelta

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
login_manager.init_app(app)  

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_comentario, nombre, comentario, fecha FROM comentarios ORDER BY fecha DESC")
    comentarios = cursor.fetchall()
    conn.close()

    return render_template('index.html', comentarios=comentarios)

@main.route('/gallery') 
def gallery():
    return render_template('gallery.html')

@main.route('/about')
def about():

    return render_template('about.html')

@main.route('/services')
def services():
    services_data = {
    'Masajes': [
        {'id': 1, 'image': 'antiStress.jpg', 'name': 'Anti-stress', 'description': 'Masaje relajante que alivia la tensión acumulada y el estrés del día a día, proporcionando una sensación de paz y bienestar.', 'price': '$40'},
        {'id': 2, 'image': 'masajeDescontracturante.jpg', 'name': 'Descontracturantes', 'description': 'Masaje profundo diseñado para liberar las contracturas musculares y aliviar el dolor en áreas tensas como espalda, cuello y hombros.', 'price': '$50'},
        {'id': 3, 'image': 'masajeConPiedrasCalientes.jpg', 'name': 'Masajes con piedras calientes', 'description': 'Terapia que utiliza piedras volcánicas calientes para relajar los músculos y mejorar la circulación sanguínea, brindando un alivio profundo.', 'price': '$60'},
        {'id': 4, 'image': 'masajeCirculatorio.jpg', 'name': 'Circulatorios', 'description': 'Masaje que mejora la circulación sanguínea y linfática, ayudando a reducir la retención de líquidos y la sensación de piernas cansadas.', 'price': '$55'}
    ],
    'Belleza': [
        {'id': 5, 'image': 'liftingPesta.jpg', 'name': 'Lifting de pestaña', 'description': 'Tratamiento que eleva y curva las pestañas de manera natural, realzando la mirada sin necesidad de utilizar rizadores o extensiones.', 'price': '$70'},
        {'id': 6, 'image': 'depilacionFacial.jpg', 'name': 'Depilación facial', 'description': 'Eliminación precisa del vello facial no deseado, dejando la piel suave y sin irritaciones.', 'price': '$30'},
        {'id': 7, 'image': 'bellezaManosYPies.jpg', 'name': 'Belleza de manos y pies', 'description': 'Tratamiento completo para embellecer y cuidar las manos y los pies, incluyendo exfoliación, hidratación y esmaltado.', 'price': '$45'}
    ],
    'Tratamientos Faciales': [
        {'id': 8, 'image': 'puntaDiamante.jpg', 'name': 'Punta de Diamante', 'description': 'Exfoliación facial no invasiva que utiliza puntas de diamante para eliminar células muertas y mejorar la textura de la piel.', 'price': '$80'},
        {'id': 9, 'image': 'limpiezaHidratacion.jpg', 'name': 'Limpieza profunda + Hidratación', 'description': 'Tratamiento facial que combina una limpieza profunda de los poros con una hidratación intensa, dejando la piel fresca y rejuvenecida.', 'price': '$90'},
        {'id': 10, 'image': 'crioFrecuencia.jpg', 'name': 'Crio frecuencia facial', 'description': 'Terapia que combina frío y radiofrecuencia para mejorar la firmeza y elasticidad de la piel, reduciendo arrugas y líneas de expresión.', 'price': '$100'}
    ],
    'Tratamientos Corporales': [
        {'id': 11, 'image': 'velaSlim.jpg', 'name': 'VelaSlim', 'description': 'Tratamiento que combina succión y energía para reducir la celulitis y moldear el contorno corporal.', 'price': '$120'},
        {'id': 12, 'image': 'dermoHealth.jpg', 'name': 'DermoHealth', 'description': 'Tecnología avanzada que mejora la oxigenación y la circulación de la piel, promoviendo una apariencia más saludable y rejuvenecida.', 'price': '$110'},
        {'id': 13, 'image': 'crioFrecuenciaCorporal.jpg', 'name': 'Criofrecuencia', 'description': 'Terapia que utiliza frío y radiofrecuencia para reducir la grasa localizada y tonificar la piel en áreas específicas del cuerpo.', 'price': '$115'},
        {'id': 14, 'image': 'ultraCavitacion.jpg', 'name': 'Ultracavitación', 'description': 'Tratamiento no invasivo que utiliza ultrasonido para eliminar la grasa localizada, mejorando el contorno corporal.', 'price': '$105'}
    ]
}

    return render_template('services.html', categories=services_data)

@main.route('/news')
def news():
    return render_template('news.html', title = 'Noticias')

@main.route('/jobs')
def jobs():
    return render_template('jobs.html')

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

        # Verificar si el email ya existe en clientes
        cursor.execute("SELECT id_cliente FROM clientes WHERE email = ?", (data['email'],))
        existing_client = cursor.fetchone()
        if existing_client is not None:
            conn.close()
            return jsonify({'success': False, 'message': 'El email ya está en uso.'})

        # Verificar si el nombre de usuario ya existe en usuarios
        cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = ?", (data['nombre_usuario'],))
        existing_user = cursor.fetchone()
        if existing_user is not None:
            conn.close()
            return jsonify({'success': False, 'message': 'El nombre de usuario ya está en uso.'})

        # Inserta el nuevo cliente
        cursor.execute("""
            INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
            VALUES (?, ?, ?, ?, ?);
        """, (data['nombre'], data['apellido'], data['email'], data['telefono'], data['direccion']))
        
        conn.commit()

        # Obtener el ID del cliente recién insertado usando el email
        cursor.execute("SELECT id_cliente FROM clientes WHERE email = ?", (data['email'],))
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

        return jsonify({'success': True, 'message': 'Registro exitoso'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    
@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user_id = current_user.id
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')

        # Asegurarnos de que ningún campo está vacío
        if not (nombre and apellido and email and telefono and direccion):
            conn.close()
            return jsonify({'success': False, 'error': 'Todos los campos son obligatorios'}), 400

        # Actualizar todos los campos sin verificar cambios individuales
        consulta_sql = """
        UPDATE clientes
        SET nombre = ?, apellido = ?, email = ?, telefono = ?, direccion = ?
        WHERE id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)
        """
        cursor.execute(consulta_sql, (nombre, apellido, email, telefono, direccion, user_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True})

    # Si el método es GET, obtener los datos actuales del cliente
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)", (user_id,))
    client_data = cursor.fetchone()
    conn.close()

    if client_data:
        return render_template('perfil.html', client=client_data)
    else:
        return "No se encontraron datos del cliente", 404

@app.route('/consulta', methods=['GET', 'POST'])
@login_required  # Asegura que el usuario esté logueado
def consulta():
    services_data = {
    'Masajes': [
        {'id': 1, 'image': 'antiStress.jpg', 'name': 'Anti-stress', 'description': 'Descripción del servicio...', 'price': '$40'},
        {'id': 2, 'image': 'masajeDescontracturante.jpg', 'name': 'Descontracturantes', 'description': 'Descripción del servicio...', 'price': '$50'},
        {'id': 3, 'image': 'masajeConPiedrasCalientes.jpg', 'name': 'Masajes con piedras calientes', 'description': 'Descripción del servicio...', 'price': '$60'},
        {'id': 4, 'image': 'masajeCirculatorio.jpg', 'name': 'Circulatorios', 'description': 'Descripción del servicio...', 'price': '$55'}
    ],
    'Belleza': [
        {'id': 5, 'image': 'liftingPesta.jpg', 'name': 'Lifting de pestaña', 'description': 'Descripción del servicio...', 'price': '$70'},
        {'id': 6, 'image': 'depilacionFacial.jpg', 'name': 'Depilación facial', 'description': 'Descripción del servicio...', 'price': '$30'},
        {'id': 7, 'image': 'bellezaManosYPies.jpg', 'name': 'Belleza de manos y pies', 'description': 'Descripción del servicio...', 'price': '$45'}
    ],
    'Tratamientos Faciales': [
        {'id': 8, 'image': 'puntaDiamante.jpg', 'name': 'Punta de Diamante', 'description': 'Descripción del servicio...', 'price': '$80'},
        {'id': 9, 'image': 'limpiezaHidratacion.jpg', 'name': 'Limpieza profunda + Hidratación', 'description': 'Descripción del servicio...', 'price': '$90'},
        {'id': 10, 'image': 'crioFrecuencia.jpg', 'name': 'Crio frecuencia facial', 'description': 'Descripción del servicio...', 'price': '$100'}
    ],
    'Tratamientos Corporales': [
        {'id': 11, 'image': 'velaSlim.jpg', 'name': 'VelaSlim', 'description': 'Descripción del servicio...', 'price': '$120'},
        {'id': 12, 'image': 'dermoHealth.jpg', 'name': 'DermoHealth', 'description': 'Descripción del servicio...', 'price': '$110'},
        {'id': 13, 'image': 'crioFrecuenciaCorporal.jpg', 'name': 'Criofrecuencia', 'description': 'Descripción del servicio...', 'price': '$115'},
        {'id': 14, 'image': 'ultraCavitacion.jpg', 'name': 'Ultracavitación', 'description': 'Descripción del servicio...', 'price': '$105'}
    ]
}
    if request.method == 'POST':
        nombre = request.form['nombre']  # El nombre se extrae del formulario
        email = request.form['email']
        titulo = request.form['titulo']
        servicio = request.form.get('servicio', '')
        mensaje = request.form['mensaje']

        # Si se seleccionó un servicio, incluirlo en el mensaje
        if servicio:
            mensaje = f"Servicio consultado: {servicio}\n\n{mensaje}"

        # Guardar la consulta en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultas (nombre, email, tituloConsulta, mensaje) VALUES (?, ?, ?, ?)", 
                       (nombre, email, titulo, mensaje))
        conn.commit()
        conn.close()

        # Redirigir a la página de consulta con un mensaje de éxito
        return redirect(url_for('consulta', success=True))
    
    # Renderizar el template con 'services_data'
    return render_template('consulta.html', success=request.args.get('success'), services_data=services_data)



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

@app.route('/mis_turnos')
@login_required
def mis_turnos():
    if current_user.rol not in ['Cliente', 'Administrador']:
        return redirect(url_for('main.index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.nombre, t.fecha, t.hora, t.estado, t.id_turno
        FROM turnos t
        JOIN servicios s ON t.id_servicio = s.id_servicio
        WHERE t.id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)
        ORDER BY t.fecha, t.hora
    """, (current_user.id,))
    turnos = cursor.fetchall()
    conn.close()

    return render_template('mis_turnos.html', turnos=turnos)


@app.route('/elegir_turno/<int:servicio_id>', methods=['GET', 'POST'])
@login_required
def elegir_turno(servicio_id):
    if current_user.rol not in ['Cliente', 'Administrador']:
        return redirect(url_for('main.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')

        # Insertar el turno en la base de datos
        cursor.execute("""
            INSERT INTO turnos (fecha, hora, id_cliente, id_servicio, estado)
            VALUES (?, ?, (SELECT id_cliente FROM usuarios WHERE id_usuario = ?), ?, 'Pendiente')
        """, (fecha, hora, current_user.id, servicio_id))
        conn.commit()
        conn.close()

        # Redirigir al usuario a la página de "Mis Turnos"
        return redirect(url_for('mis_turnos'))
    
    # Si el método es GET, mostrar la página para elegir turno
    cursor.execute("SELECT nombre, duracion, precio FROM servicios WHERE id_servicio = ?", (servicio_id,))
    servicio = cursor.fetchone()
    conn.close()

    return render_template('elegir_turno.html', servicio=servicio, servicio_id=servicio_id)

@app.route('/cancelar_turno/<int:turno_id>', methods=['POST'])
@login_required
def cancelar_turno(turno_id):
    if current_user.rol not in ['Cliente', 'Administrador']:
        return redirect(url_for('main.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Eliminar el turno
    cursor.execute("DELETE FROM turnos WHERE id_turno = ? AND id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)", (turno_id, current_user.id))
    conn.commit()
    conn.close()

    return redirect(url_for('mis_turnos'))


@app.route('/modificar_turno/<int:turno_id>', methods=['POST'])
@login_required
def modificar_turno(turno_id):
    if current_user.rol not in ['Cliente', 'Administrador']:
        return redirect(url_for('main.index'))

    nueva_fecha = request.form['fecha']
    nueva_hora = request.form['hora']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, hora FROM turnos WHERE id_turno = ? AND id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)", (turno_id, current_user.id))
    turno = cursor.fetchone()

    # turno[0] ya es un objeto datetime.date y turno[1] ya es un objeto datetime.time
    turno_datetime = datetime.combine(turno[0], turno[1])
    if turno_datetime < datetime.now() + timedelta(hours=24):
        conn.close()
        flash('No puedes modificar un turno con menos de 24 horas de antelación.', 'danger')
        return redirect(url_for('mis_turnos'))

    cursor.execute("""
        UPDATE turnos
        SET fecha = ?, hora = ?
        WHERE id_turno = ? AND id_cliente = (SELECT id_cliente FROM usuarios WHERE id_usuario = ?)
    """, (nueva_fecha, nueva_hora, turno_id, current_user.id))
    conn.commit()
    conn.close()

    flash('Turno modificado con éxito.', 'success')
    return redirect(url_for('mis_turnos'))

def convertir_a_hora_argentina(utc_datetime):
    # UTC-3 para Argentina Standard Time
    return utc_datetime - timedelta(hours=3)

from sqlalchemy.sql import text
from datetime import datetime, timedelta

def convertir_a_hora_argentina(utc_datetime):
    return utc_datetime - timedelta(hours=3)

@main.route('/submit_comment', methods=['POST'])
def submit_comment():
    nombre = request.form.get('nombre')
    comentario = request.form.get('comentario')

    if not nombre and current_user.is_authenticated:
        nombre = current_user.nombre_usuario
    if not nombre:
        nombre = "Anónimo"

    # Escapar caracteres especiales en la cadena para evitar errores en la consulta
    nombre = nombre.replace("'", "''")
    comentario = comentario.replace("'", "''")

    # Insertar el comentario en la base de datos
    insert_query = text(
        "INSERT INTO comentarios (nombre, comentario) VALUES (:nombre, :comentario);"
    )
    select_query = text(
        "SELECT TOP 1 nombre, fecha FROM comentarios ORDER BY id_comentario DESC"
    )

    with engine.connect() as conn:
        conn.execute(insert_query, {'nombre': nombre, 'comentario': comentario})
        conn.commit()
        # Obtener el comentario recién insertado
        nuevo_comentario = conn.execute(select_query).fetchone()

    if nuevo_comentario:
        # Convertir la hora a la zona horaria de Argentina
        fecha_local = convertir_a_hora_argentina(nuevo_comentario[1])  # Accede con índice [1] para la fecha
        # Formatear la fecha para la respuesta
        fecha_formateada = fecha_local.strftime('%d/%m/%Y %H:%M')
        return jsonify({'nombre': nuevo_comentario[0], 'comentario': comentario, 'fecha': fecha_formateada})  # Accede con índice [0] para el nombre
    else:
        return jsonify({'error': 'Error al insertar el comentario.'}), 500


