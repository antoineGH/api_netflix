from flask import Blueprint, jsonify, request, render_template
from media.utils import getExternal, getSimilar, getMedias, getMedia, postMedia, deleteMedia
from flask_jwt_extended import jwt_required, get_jwt_claims
from models import List, User, Media

media = Blueprint('media', __name__)

@media.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@media.route('/api/<string:type_media>/<string:media_id>/external_ids', methods=['GET'])
def getExternalMain(type_media, media_id):
    if type_media not in ['media', 'tv']:
        return jsonify({'msg':'type_media should be media or tv'})
    external = getExternal(type_media, media_id)
    return jsonify(external)

@media.route('/api/<string:type_media>/<string:media_id>/similar', methods=['GET'])
def getSimilarMain(type_media, media_id):
    if type_media not in ['media', 'tv']:
        return jsonify({'msg':'type_media should be media or tv'})

    language = request.args.get('language', 'en-US')
    
    similars = getSimilar(type_media, media_id, language)
    return jsonify(similars)

@media.route('/api/medias/<int:list_id>', methods=['GET'])
@jwt_required
def get_medias(list_id):
    
    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    if not list_id:
        return jsonify({"msg": "Missing list_id in request"}), 400

    users = User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)

    if not list:
        return jsonify({"msg": "List not found"}), 404

    accountHasList = False
    for user in users:
        if user.user_id == list.user_id:
            accountHasList = True
        
    if not accountHasList:
        return jsonify({'msg':'Unauthorized'}), 500

    return getMedias(account_id, list_id)

@media.route('/api/media', methods=['POST'])
@jwt_required
def media_post():
    if not request.is_json: 
        return jsonify({"msg": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    tmdb_id = content.get("tmdb_id", None)
    media_type = content.get("media_type", None)
    list_id = content.get("list_id", None)

    if not tmdb_id:
        return jsonify({"msg": "Missing tmdb_id"}), 400
    if not media_type or media_type not in ['video', 'tv']:
        return jsonify({"msg": "Missing media_type"}), 400
    if not list_id:
        return jsonify({"msg": "Missing list_id"}), 400

    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    users = User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)

    if not list:
        return jsonify({"msg": "List not found"}), 404

    accountHasList = False
    for user in users:
        if user.user_id == list.user_id:
            accountHasList = True
        
    if not accountHasList:
        return jsonify({'msg':'Unauthorized'}), 500

    return postMedia(tmdb_id, media_type, list_id)

@media.route('/api/media/<int:media_id>', methods=['GET', 'DELETE'])
@jwt_required
def media_user(media_id):

    if not media_id:
        return jsonify({"msg": "Missing media_id in request"}), 400

    claims = get_jwt_claims()
    account_id = claims.get('account_id')

    if not account_id:
        return jsonify({'msg': 'Missing account_id in Token'}), 400

    media = Media.query.get(media_id)
    if not media:
        return jsonify({'msg':'Media not found'})

    list = List.query.get(media.list_id)
    if not list:
        return jsonify({"msg": "List not found"}), 404
        
    users = User.query.filter_by(account_id=account_id).all()

    accountHasList = False
    for user in users:
        if user.user_id == list.user_id:
            accountHasList = True
        
    if not accountHasList:
        return jsonify({'msg':'Unauthorized'}), 500

    if request.method == 'GET':
        return getMedia(media_id)

    if request.method == 'DELETE':
        return deleteMedia(media_id)