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


