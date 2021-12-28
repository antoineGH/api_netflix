from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getTrending(type, time_window):
    url = f'https://api.themoviedb.org/3/trending/{type}/{time_window}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()