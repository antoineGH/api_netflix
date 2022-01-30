from flask import jsonify
from models import User, Media, List
from __init__ import db

def getUsers(account_id):
    users = User.query.filter_by(account_id=account_id).all()
    if not users:
        return jsonify({"msg": "No user for this account"}), 400
    return jsonify([user.serialize for user in users])

def getUser(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize)

def postUser(profile, account_id):
    users = User.query.filter_by(account_id=account_id).all()
    if len(users) >= 5:
        return jsonify({"msg": "No more than 5 profiles"}), 400

    for user in users:
        if user.profile == profile:
            return jsonify({"msg": "Profile name already exist for account"}), 400
    user = User(profile=profile, account_id=account_id)
    db.session.add(user)
    try:
        db.session.commit()
        list = List(list_title="{}'s list".format(profile), user_id=user.user_id)
        db.session.add(list)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"msg": "Couldn't add list to DB"}), 400 
        return jsonify(user.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add user to DB"}), 400

def updateUser(user_id, profile):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"msg": "User not found"}), 404
    user.profile = profile
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't update user"})

def deleteUser(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"msg": "User not found"}), 404

    lists = List.query.filter_by(user_id=user_id).all()
    for list in lists:
        movies = Movie.query.filter_by(list_id=list.list_id).all()
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
        except:
            db.session.rollback()
            return jsonify(False)
    db.session.delete(user)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)