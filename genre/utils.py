from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getGenreMediaList(type_media, language):
    url = f'https://api.themoviedb.org/3/genre/{type_media}/list?language={language}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()
