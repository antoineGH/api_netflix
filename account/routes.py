import json
from os import access
from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, create_access_token
from account.utils import login, register, getAccount, updateAccount, deleteAccount
account = Blueprint('account', __name__)

@account.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@account.route('/api/login', methods=['POST'])
def account_login():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400
    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    return login(email, password)

@account.route('/api/register', methods=['POST'])
def account_register():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    first_name = content.get("first_name", None)
    last_name = content.get("last_name", None)

    if not email:
        return jsonify({"msg": "Missing Email"}), 400
    if not password:
        return jsonify({"msg": "Missing Password"}), 400
    if not first_name:
        return jsonify({"msg": "Missing First name"}), 400
    if not last_name:
        return jsonify({"msg": "Missing Last name"}), 400

    return register(email, first_name, last_name, password)

@account.route('/api/account', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def account_user():
    claims = get_jwt_claims()
    account_id = claims.get('account_id')
    
    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    if request.method == 'GET':
        return getAccount(account_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        first_name = content['first_name'] if 'first_name' in content.keys() else ''
        last_name = content['last_name'] if 'last_name' in content.keys() else ''
        password = content['password'] if 'password' in content.keys() else ''
        return updateAccount(password, first_name, last_name, account_id)

    if request.method == 'DELETE':
        return deleteAccount(account_id)