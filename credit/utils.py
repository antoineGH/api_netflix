from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getCredits(credit_id):
    url = f'https://api.themoviedb.org/3/credit/{credit_id}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getCreditID(type_media, media_id):
    url = f'https://api.themoviedb.org/3/{type_media}/{media_id}/credits'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()