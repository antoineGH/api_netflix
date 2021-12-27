from flask import Blueprint, jsonify
from movies.utils import get_movie

movies = Blueprint('movies', __name__)

@movies.route('/api/movie/<int:movie_id>', methods=['GET'])
def movie_id(movie_id):
    if not movie_id:
        return jsonify({'message': 'missing movie_id in request'}), 404

    movies = get_movie(movie_id)
    return jsonify({'movies': movies})