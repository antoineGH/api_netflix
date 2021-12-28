from flask import Blueprint, jsonify
from flask import request 
import requests
from movie.utils import searchMovie, getDetails

movie = Blueprint('movie', __name__)

@movie.route('/api/search/movie', methods=['GET'])
def searchMovieMain():
    query = request.args.get('query')
    print(query)
    if not query:
        return jsonify({'message':'missing query in request'})
    movies = searchMovie(query)
    return jsonify(movies)

@movie.route('/api/search/movie/<int:movie_id>', methods=['GET'])
def getDetailsMain(movie_id):
    if not movie_id:
        return jsonify({'message': 'missing movie_id in request'}), 404
    movie = getDetails(movie_id)
    return jsonify(movie)