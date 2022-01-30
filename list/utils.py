from flask import jsonify
from models import User, List, Media
from __init__ import db

def getLists(account_id, user_id):
    users = User.query.filter_by(account_id=account_id).all()
    user_in_account = False
    for user in users:
        if user.user_id == user_id:
            user_in_account=True  
    if not user_in_account:
        return jsonify({"msg": "This user not in Account"}), 503
    lists = List.query.filter_by(user_id=user_id).all()
    return jsonify([list.serialize for list in lists])

def getList(list_id):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"msg": "List not found"}), 404
    return jsonify(list.serialize)

def postList(list_title, user_id):
    lists = List.query.filter_by(user_id=user_id).all()
    for list in lists:
        if list.list_title == list_title:
            return jsonify({"msg": "List title already exist for user"}), 400
    list = List(list_title=list_title, user_id=user_id)
    db.session.add(list)
    try:
        db.session.commit()
        return jsonify(list.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add list to DB"}), 400

def updateList(list_id, list_title):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"msg": "List not found"}), 404
    list.list_title = list_title
    db.session.add(list)
    try:
        db.session.commit()
        return jsonify(list.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't update list"})

def deleteList(list_id):
    list = List.query.get(list_id)
    if not list: 
        return jsonify({"msg": "List not found"}), 404
    movies = Media.query.filter_by(list_id=list_id).all()
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