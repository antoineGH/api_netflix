from flask import current_app
import requests
import urllib.parse
from auth.BearerAuth import BearerAuth

def getGenreList(language):
    encoded = urllib.parse.quote(language)
    url = f'https://api.themoviedb.org/3/genre/movie/list?language={encoded}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

