from flask import current_app
import requests
import urllib.parse
from werkzeug.wrappers import response
from auth import BearerAuth

def searchMovie(query):
    encoded = urllib.parse.quote(query)
    url = f"https://api.themoviedb.org/3/search/movie?query={encoded}"
    print(url)
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getDetails(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()