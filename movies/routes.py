from flask import Blueprint, jsonify
from movies.utils import get_movies

movies = Blueprint('movies', __name__)

@movies.route('/api/movies', methods=['GET'])
def api_movies():
    movies = get_movies()
    return jsonify({'movies': movies})