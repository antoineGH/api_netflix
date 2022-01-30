from flask import jsonify
from flask_jwt_extended import create_access_token
from models import Account, User, List, Media
from __init__ import db, bcrypt, jwt

def login(email, password):
    if not email: 
        return jsonify({"msg": "Missing Email"}), 400
    if not password: 
        return jsonify({"msg": "Missing Password"}), 400
    account = Account.query.filter_by(email=email).first()
    if not account: 
        return jsonify({"msg": "Account not found"}), 404
    if account.password == '':
        return jsonify({"msg": "Account not active, Set a password"}), 401
    if not bcrypt.check_password_hash(account.password, password):
        return jsonify({"msg": "Wrong email or password"}), 401
    ret = {
        'access_token': create_access_token(identity=email),
    }
    return jsonify(ret), 201

def register(email, first_name, last_name, password):
    accountExisting = Account.query.filter_by(email=email).first()
    if accountExisting:
        return jsonify({'msg': 'Account already exists'}), 400
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    account = Account(email=email, password=hashedPassword, first_name=first_name, last_name=last_name)
    db.session.add(account)
    
    try:
        db.session.commit()
        user = User(profile=first_name, account_id=account.account_id)
        db.session.add(user)
        try:
            db.session.commit()
            list = List(list_title="{}'s list".format(first_name), user_id=user.user_id)
            db.session.add(list)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"msg": "Couldn't add list to DB"}), 400 
        except:
            db.session.rollback()
            return jsonify({"msg": "Couldn't add user to DB"}), 400

        return jsonify(account.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add account to DB"}), 400

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    account = Account.query.filter_by(email=identity).first()
    return {
        'account_id' : account.account_id,
        'email': account.email,
        'first_name' : account.first_name,
        'last_name' : account.last_name,
    }

def getAccount(account_id):
    account = Account.query.get(account_id)
    if not account: 
        return jsonify({"msg": "Account not found"}), 404
    return jsonify(account.serialize)

def updateAccount(password, first_name, last_name, account_id):
    account = Account.query.get(account_id)
    if not account: 
        return jsonify({"msg": "Account not found"}), 404
    if first_name:
        account.first_name = first_name
    if last_name:
        account.last_name = last_name
    if password:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        account.password = hashed_password
    db.session.add(account)
    try:
        db.session.commit()
        return jsonify(account=account.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add account to DB"})

def deleteAccount(account_id):
    account = Account.query.get(account_id)
    if not account: 
        return jsonify({"msg": "Account not found"}), 404

    users = User.query.filter_by(account_id=account_id).all()
    for user in users:
        lists = List.query.filter_by(user_id=user.user_id).all()
        for list in lists:
            movies = Media.query.filter_by(list_id=list.list_id).all()
            for movie in movies:
                if movie:
                    db.session.delete(movie)
                    try:
                        db.session.commit()
                    except:
                        return jsonify(False)
            if list:
                db.session.delete(list)
                try:
                    db.session.commit()
                except:
                    return jsonify(False)
        if user:
            db.session.delete(user)
            try:
                db.session.commit()
            except:
                return jsonify(False)
    db.session.delete(account)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)

