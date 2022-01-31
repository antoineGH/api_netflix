from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getExternal(type_media, media_id):
    url = f'https://api.themediadb.org/3/{type_media}/{media_id}/external_ids'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getSimilar(type_media, media_id, language):
    url = f'https://api.themediadb.org/3/{type_media}/{media_id}/similar?language={language}&page=1'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

from flask import jsonify
from models import Media, User, List
from __init__ import db

def getMedias(account_id, list_id):
    users= User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)
    for user in users:
        if user.user_id == list.user_id:
            user_in_account=True  
    if not user_in_account:
        return jsonify({"msg": "This user not in Account"}), 503

    medias = Media.query.filter_by(list_id=list_id).all()
    return jsonify([media.serialize for media in medias])

def getMedia(media_id):
    media = Media.query.get(media_id)
    if not media: 
        return jsonify({"msg": "Media not found"}), 404
    return jsonify(media.serialize)

def postMedia(tmdb_id, media_type, list_id):
    medias = Media.query.filter_by(list_id=list_id).all()
    for media in medias:
        if media.tmdb_id == tmdb_id:
            return jsonify({"msg": "Media already in list"}), 400
    media = Media(tmdb_id=tmdb_id, media_type=media_type, list_id=list_id)
    db.session.add(media)
    try:
        db.session.commit()
        return jsonify(media.serialize)
    except:
        db.session.rollback()
        return jsonify({"msg": "Couldn't add media to DB"}), 400

def deleteMedia(media_id):
    media = Media.query.get(media_id)
    if not media: 
        return jsonify({"msg": "Media not found"}), 404
    db.session.delete(media)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)