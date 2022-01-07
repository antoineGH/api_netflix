from flask import jsonify
from models import List, Movie
from __init__ import db

def getList(list_id):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"message": "List not found"}), 404
    return jsonify(list=list.serialize)

def postList(list_title, user_id):
    lists = List.query.filter_by(user_id=user_id).all()
    for list in lists:
        if list.list_title == list_title:
            return jsonify({"message": "List title already exist for user"}), 400
    list = List(list_title=list_title, user_id=user_id)
    db.session.add(list)
    try:
        db.session.commit()
        return jsonify(list=list.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add list to DB"}), 400

def updateList(list_id, list_title):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"message": "List not found"}), 404
    list.list_title = list_title
    db.session.add(list)
    try:
        db.session.commit()
        return jsonify(list=list.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't update list"})

def deleteList(list_id):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"message": "List not found"}), 404
    movies = Movie.query.filter_by(list_id=list_id).all()
    for movie in movies:
        db.session.delete(movie)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(False)
    db.session.delete(list)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)