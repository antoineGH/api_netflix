from flask import current_app, jsonify
import requests
from auth.BearerAuth import BearerAuth
from models import Media, User, List
from __init__ import db


def getExternal(type_media, media_id):
    url = f'https://api.themediadb.org/3/{type_media}/{media_id}/external_ids'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getSimilar(type_media, media_id, language):
    url = f'https://api.themediadb.org/3/{type_media}/{media_id}/similar?language={language}&page=1'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getMedias(account_id, list_id):
    users= User.query.filter_by(account_id=account_id).all()
    list = List.query.get(list_id)
    for user in users:
        if user.user_id == list.user_id:
            user_in_account=True  
    if not user_in_account:
        return jsonify({"msg": "This user not in Account"}), 503

    medias = Media.query.filter_by(list_id=list_id).all()
    print(medias)

    for media in medias:
        url = f'https://api.themoviedb.org/3/{media.media_type}/{media.tmdb_id}?language=en-US'
        response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
        media_details = response.json()
        media.imdb_id = media_details.get("imdb_id", None)
        media.genres = media_details.get("genres", None)
        media.title = media_details.get("title", None)
        media.original_language = media_details.get("original_language", None)
        media.tagline = media_details.get("tagline", None)
        media.homepage = media_details.get("homepage", None)
        media.overview = media_details.get("overview", None)
        media.runtime = media_details.get("runtime", None)
        media.release_date = media_details.get("release_date", None)
        media.production_countries = media_details.get("production_countries", None)
        media.production_companies = media_details.get("production_companies", None)
        media.poster_path = media_details.get("poster_path", None)
        media.poster_full_path = "https://image.tmdb.org/t/p/w500/" + media.poster_path
        media.vote_average = media_details.get("vote_average", None)
        media.vote_count = media_details.get("vote_count", None)
        media.popularity = media_details.get("popularity", None)
        media.video = media_details.get("video", None)
        media.status = media_details.get("status", None)
        
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