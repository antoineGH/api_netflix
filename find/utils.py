from flask import current_app
import requests
import urllib.parse
from auth.BearerAuth import BearerAuth

def searchMedias(type_media, query):
    encoded = urllib.parse.quote(query)
    url = f"https://api.themoviedb.org/3/search/{type_media}?query={encoded}"
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getDetails(type_media, movie_id):
    url = f"https://api.themoviedb.org/3/{type_media}/{movie_id}"
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()