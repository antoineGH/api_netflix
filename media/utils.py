from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getExternal(type_media, media_id):
    url = f'https://api.themoviedb.org/3/{type_media}/{media_id}/external_ids'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getSimilar(type_media, media_id, language):
    url = f'https://api.themoviedb.org/3/{type_media}/{media_id}/similar?language={language}&page=1'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()