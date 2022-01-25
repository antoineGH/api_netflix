from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from movie.utils import getMovies, getMovie, postMovie, deleteMovie
from models import List, User

movie = Blueprint('movie', __name__)

@movie.route('/api/movies/<int:list_id>', methods=['GET'])
@jwt_required
def get_movies(list_id):
    
    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    if not list_id:
        return jsonify({"msg": "Missing list_id in request"}), 400

    users = User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)

    if not list:
        return jsonify({"msg": "List not found"}), 404

    accountHasList = False
    for user in users:
        if user.user_id == list.user_id:
            accountHasList = True
        
    if not accountHasList:
        return jsonify({'msg':'Unauthorized'}), 500



    return getMovies(account_id, list_id)

@movie.route('/api/movie', methods=['POST'])
@jwt_required
def movie_post():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    tmdb_id = content.get("tmdb_id", None)
    list_id = content.get("list_id", None)

    if not tmdb_id:
        return jsonify({"msg": "Missing tmdb_id"}), 400
    if not list_id:
        return jsonify({"msg": "Missing list_id"}), 400

    return postMovie(tmdb_id, list_id)

@movie.route('/api/movie/<int:movie_id>', methods=['GET', 'DELETE'])
@jwt_required
def movie_user(movie_id):

    if not movie_id:
        return jsonify({"msg": "Missing movie_id in request"}), 400

    if request.method == 'GET':
        return getMovie(movie_id)

    if request.method == 'DELETE':
        return deleteMovie(movie_id)