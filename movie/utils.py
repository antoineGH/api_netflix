from flask import jsonify
from models import Movie
from __init__ import db

def getMovie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie: 
        return jsonify({"message": "Movie not found"}), 404
    return jsonify(movie=movie.serialize)

def postMovie(tmdb_id, list_id):
    movie = Movie(tmdb_id=tmdb_id, list_id=list_id)
    db.session.add(movie)
    try:
        db.session.commit()
        return jsonify(movie=movie.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add movie to DB"}), 400

def deleteMovie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie: 
        return jsonify({"message": "Movie not found"}), 404
    db.session.delete(movie)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)