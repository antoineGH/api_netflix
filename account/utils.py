from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from models import Account
from __init__ import db, bcrypt, jwt

def login(email, password):
    if not email: 
        return jsonify({"message": "Missing Email"}), 400
    if not password: 
        return jsonify({"message": "Missing Password"}), 400
    account = Account.query.filter_by(email=email).first()
    if not account: 
        return jsonify({"message": "Account not found"}), 404
    if account.password == '':
        return jsonify({"message": "Account not active, Set a password"}), 401
    if not bcrypt.check_password_hash(account.password, password):
        return jsonify({"message": "Wrong email or password"}), 401
    ret = {
        'access_token': create_access_token(identity=email),
    }
    return jsonify(ret), 201

def register(email, first_name, last_name, password):
    accountExisting = Account.query.filter_by(email=email).first()
    if accountExisting:
        return jsonify({'message': 'Account already exists'}), 400
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    account = Account(email=email, password=hashedPassword, first_name=first_name, last_name=last_name)
    db.session.add(account)
    try:
        db.session.commit()
        return jsonify(account=account.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add account to DB"}), 400

@jwt.account_claims_loader
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
        return jsonify({"message": "Account not found"}), 404
    return jsonify(account=account.serialize)

def updateAccount(password, first_name, last_name, account_id):
    account = Account.query.get(account_id)
    if not account: 
        return jsonify({"message": "Account not found"}), 404
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
        return jsonify({"message": "Couldn't add account to DB"})

def deleteAccount(account_id):
    account = Account.query.get(account_id)
    if not account: 
        return jsonify({"message": "Account not found"}), 404
    db.session.delete(account)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)

