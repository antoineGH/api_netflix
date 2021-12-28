from flask import Blueprint, jsonify
from flask import request 
import requests
from movies.utils import search_movie_id, search_movie, get_genre_list

movies = Blueprint('movies', __name__)

@movies.route('/api/search/movie', methods=['GET'])
def searchMovie():
    query = request.args.get('query')
    print(query)
    if not query:
        return jsonify({'message':'missing query in request'})
    
    movies = search_movie(query)
    return jsonify(movies)

@movies.route('/api/search/movie/<int:movie_id>', methods=['GET'])
def searchMovieId(movie_id):
    if not movie_id:
        return jsonify({'message': 'missing movie_id in request'}), 404

    movie = search_movie_id(movie_id)
    return jsonify(movie)

@movies.route('/api/genre/list', methods=['GET'])
def getGenreList():
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    genre_list = get_genre_list(language)
    return jsonify(genre_list)

