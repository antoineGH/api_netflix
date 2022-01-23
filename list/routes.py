from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from sqlalchemy.sql.functions import user
from list.utils import getLists, getList, postList, updateList, deleteList
from models import User, List

list = Blueprint('list', __name__)

@list.route('/api/lists/<int:user_id>', methods=['GET'])
@jwt_required
def get_lists(user_id):
    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    if not user_id:
        return jsonify({"msg": "Missing user_id in request"}), 400

    users = User.query.filter_by(account_id=account_id).all()
    accountHasUser = False
    for user in users:
        if user.user_id == user_id:
            accountHasUser = True

    if not accountHasUser:
        return jsonify({"msg": "Unauthorized"}), 500
        
    return getLists(account_id, user_id)
    
@list.route('/api/list', methods=['POST'])
@jwt_required
def list_post():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400

    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    content = request.get_json(force=True)
    list_title = content.get("list_title", None)
    user_id = content.get("user_id", None)

    if not list_title:
        return jsonify({"msg": "Missing list_title"}), 400
    if not user_id:
        return jsonify({"msg": "Missing user_id"}), 400

    users = User.query.filter_by(account_id=account_id).all()
    accountHasUser = False
    for user in users:
        if user_id == user.user_id:
            accountHasUser = True

    if not accountHasUser:
        return jsonify({"msg": "Unauthorized"}), 500

    return postList(list_title, user_id)

@list.route('/api/list/<int:list_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def list_user(list_id):

    if not list_id:
        return jsonify({"msg": "Missing list_id in request"}), 404

    claims = get_jwt_claims()
    account_id = claims.get('account_id')
    users = User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)
    if not list:
        return jsonify({"msg": "List not existing"}), 404

    userHasList = False
    for user in users:
        if list.user_id == user.user_id:
            userHasList = True

    if not userHasList:
        return jsonify({'msg':'Unauthorized'}), 500


    if request.method == 'GET':
        return getList(list_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        list_title = content.get("list_title", None)
        if not list_title:
            return jsonify({"msg": "Missing list_title"}), 400
        return updateList(list_id, list_title)

    if request.method == 'DELETE':
        return deleteList(list_id)
