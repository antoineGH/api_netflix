from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from user.utils import getUsers, getUser, postUser, updateUser, deleteUser
from models import User

user = Blueprint('user', __name__)

@user.route('/api/users', methods=['GET'])
@jwt_required
def get_users():
    claims = get_jwt_claims()
    account_id = claims.get('account_id')
    
    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400
    return getUsers(account_id)

@user.route('/api/user', methods=['POST'])
@jwt_required
def user_post():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    profile = content.get("profile", None)
    account_id = content.get("account_id", None)

    if not profile:
        return jsonify({"msg": "Missing profile"}), 400
    if not account_id:
        return jsonify({"msg": "Missing account_id"}), 400

    return postUser(profile, account_id)

@user.route('/api/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def list_user(user_id):

    if not user_id:
        return jsonify({"msg": "Missing user_id in request"}), 404

    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    users = User.query.filter_by(account_id=account_id).all()
    accountHasUser = False
    for user in users:
        if user.user_id == user_id:
            accountHasUser=True

    if not accountHasUser:    
        return jsonify({'msg':'Unauthorized'}), 500

    if request.method == 'GET':
        return getUser(user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        profile = content.get("profile", None)
        if not profile:
            return jsonify({"msg": "Missing profile"}), 400
        return updateUser(user_id, profile)

    if request.method == 'DELETE':
        return deleteUser(user_id)
