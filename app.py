from flask import Flask, json, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS
from werkzeug import exceptions
import requests
from pprint import pprint
app = Flask(__name__)
# CORS(app)


@app.route('/')
def home():
    api_key = '6e039ddaa59376174e446308a9078ce7'
    resp = requests.get(
        f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1&include_adult=false')

    data = resp.json()
    pprint(data['results'])
    title = 'List of popular movies'
    return render_template('home.html', title=title, data=data['results'])


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    api_key = '6e039ddaa59376174e446308a9078ce7'

    resp = requests.get(
        f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US')
    data = resp.json()
    return render_template('search.html', genre_data=data['genres'])


@app.route('/searchByGenre', methods=['POST'])
def searchByGenre():
    api_key = '6e039ddaa59376174e446308a9078ce7'
    genre_id = request.form.get('genreOption')
    resp = requests.get(
        f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&include_adult=false')
    data = resp.json()
    title = "Current selected Genre: "
    return render_template('home.html', title=title, data=data['results'])


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({'message': f'Apologies for the missing data. error: {err}. Please contact:'})


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({'message': f'Its not you, its us. error: {err}'})


if __name__ == '__main__':
    app.run(debug=True)
