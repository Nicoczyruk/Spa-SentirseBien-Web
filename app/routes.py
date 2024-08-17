from flask import Blueprint, render_template


main = Blueprint('main', __name__)

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

@main.route('/contact')
def contact():
    return render_template('contact.html')

