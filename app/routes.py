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
    services_data = [
        {
            'image': 'testimonials-1.jpg',
            'name': 'Masaje Relajante',
            'description': 'Un masaje para aliviar el estrés y mejorar la circulación.',
            'price': '$50'
        },
        {
            'image': 'testimonials-2.jpg',
            'name': 'Tratamiento Facial',
            'description': 'Revitaliza tu piel con nuestros tratamientos faciales.',
            'price': '$70'
        },
        {
            'image': 'testimonials-3.jpg',
            'name': 'Pedicura',
            'description': 'Cuida tus pies con nuestra pedicura profesional.',
            'price': '$30'
        }
    ]

    return render_template('services.html', services=services_data)

@main.route('/news')
def news():
    return render_template('news.html')

@main.route('/jobs')
def jobs():
    return render_template('jobs.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')