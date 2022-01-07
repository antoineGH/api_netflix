from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from account.utils import login, register, getAccount, updateAccount, deleteAccount
account = Blueprint('account', __name__)

@account.route('/api/login', methods=['POST'])
def account_login():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400
    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    return login(email, password)

@account.route('/api/register', methods=['POST'])
def account_register():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    first_name = content.get("first_name", None)
    last_name = content.get("last_name", None)

    if not email:
        return jsonify({"message": "Missing Email"}), 400
    if not password:
        return jsonify({"message": "Missing Password"}), 400
    if not first_name:
        return jsonify({"message": "Missing First name"}), 400
    if not last_name:
        return jsonify({"message": "Missing Last name"}), 400

    return register(email, first_name, last_name, password)

@account.route('/api/account', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def account_user():
    claims = get_jwt_claims()
    account_id = claims.get('account_id')
    
    if not account_id:
        return jsonify({'message': 'Missing account_id in Token'}), 400

    if request.method == 'GET':
        return getAccount(account_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        first_name = content['first_name'] if 'first_name' in content.keys() else ''
        last_name = content['last_name'] if 'last_name' in content.keys() else ''
        password = content['password'] if 'password' in content.keys() else ''
        return updateAccount(password, first_name, last_name, account_id)

    if request.method == 'DELETE':
        return deleteAccount(account_id)
