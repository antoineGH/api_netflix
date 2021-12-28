from flask import Blueprint, jsonify
from flask import request 
import requests
from movies.utils import get_movie_id, get_movies

movies = Blueprint('movies', __name__)

# http://127.0.0.1:5000/api/movies?query=Jack+Reacher
@movies.route('/api/movies', methods=['GET'])
def getMovies():
    query = request.args.get('query')
    print(query)
    if not query:
        return jsonify({'message':'missing query in request'})
    
    movies = get_movies(query)
    return jsonify(movies)

# http://127.0.0.1:5000/api/movie/76341
@movies.route('/api/movie/<int:movie_id>', methods=['GET'])
def getMovieId(movie_id):
    if not movie_id:
        return jsonify({'message': 'missing movie_id in request'}), 404

    movie = get_movie_id(movie_id)
    return jsonify(movie)