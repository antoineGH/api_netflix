from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from sqlalchemy.sql.functions import user
from list.utils import getLists, getList, postList, updateList, deleteList

list = Blueprint('list', __name__)

@list.route('/api/lists/<int:user_id>', methods=['GET'])
@jwt_required
def get_lists(user_id):
    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'message': 'Missing account_id in Token'}), 400

    if not user_id:
        return jsonify({"message": "Missing user_id in request"}), 400

    return getLists(account_id, user_id)
    
@list.route('/api/list', methods=['POST'])
@jwt_required
def list_post():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    list_title = content.get("list_title", None)
    user_id = content.get("user_id", None)

    if not list_title:
        return jsonify({"message": "Missing list_title"}), 400
    if not user_id:
        return jsonify({"message": "Missing user_id"}), 400

    return postList(list_title, user_id)

@list.route('/api/list/<int:list_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def list_user(list_id):

    if not list_id:
        return jsonify({"message": "Missing list_id in request"}), 404

    if request.method == 'GET':
        return getList(list_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        list_title = content.get("list_title", None)
        if not list_title:
            return jsonify({"message": "Missing list_title"}), 400
        return updateList(list_id, list_title)

    if request.method == 'DELETE':
        return deleteList(list_id)
