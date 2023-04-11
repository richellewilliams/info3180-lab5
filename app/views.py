"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory, url_for
import os
from app.models import Movie
from app.forms import MovieForm
from werkzeug.utils import secure_filename
import datetime
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route("/api/v1/movies", methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        created_at = datetime.datetime.now()

        movie = Movie(title, description, filename, created_at)
        db.session.add(movie)
        db.session.commit()

        movies = db.session.execute(db.select(Movie)).scalars()
        movies_data = []
        for movie in movies:
            movies_data.append({
                "message": "Movie Successfully added",
                "title": movie.title,
                "description": movie.description,
                "poster": movie.poster
            })

        return jsonify(data=movies_data)
    else:
        return form_errors(form)


@app.route('/api/v1/movies', methods=['GET'])
def add_movies():
    movies = db.session.execute(db.select(Movie)).scalars()
    movie_data = []
    for movie in movies:
            movie_data.append({
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "poster": url_for('getPosterImage', filename=movie.poster)
            })
    return jsonify(data=movie_data)


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/posters/<path:filename>')
def getPosterImage(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    errors = []
    for field, error in form.errors.items():
        errors.append({
            "field": field,
            "message": error[0]
        })

    return jsonify(errors=errors)


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404