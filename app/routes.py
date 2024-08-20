from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import app, engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import text

main = Blueprint('main', __name__)
# Configurar logging para debugging
logging.basicConfig(level=logging.DEBUG)

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
    return render_template('news.html')

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
