from flask import jsonify
from models import Media, User, List
from __init__ import db

def getMovies(account_id, list_id):
    users= User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)
    for user in users:
        if user.user_id == list.user_id:
            user_in_account=True  
    if not user_in_account:
        return jsonify({"msg": "This user not in Account"}), 503

    movies = Media.query.filter_by(list_id=list_id).all()
    return jsonify([movie.serialize for movie in movies])

def getMovie(movie_id):
    movie = Media.query.get(movie_id)
    if not movie: 
        return jsonify({"msg": "Media not found"}), 404
    return jsonify(movie.serialize)

def postMovie(tmdb_id, list_id):
    movies = Media.query.filter_by(list_id=list_id).all()
    for movie in movies:
        if movie.tmdb_id == tmdb_id:
            return jsonify({"msg": "Media already in list"}), 400
    movie = Media(tmdb_id=tmdb_id, list_id=list_id)
    db.session.add(movie)
    try:
        db.session.commit()
        return jsonify(movie.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add movie to DB"}), 400

def deleteMovie(movie_id):
    movie = Media.query.get(movie_id)
    if not movie: 
        return jsonify({"msg": "Media not found"}), 404
    db.session.delete(movie)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)