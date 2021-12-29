from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getDiscoverMedia(type_media, language, sort_by, year, with_genres):
    url = f'https://api.themoviedb.org/3/discover/{type_media}?language={language}&sort_by={sort_by}&year={year}&with_genres={with_genres}&include_adult=false'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()