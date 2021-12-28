from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getMovieByGenre(genre, language):
    url = f'https://api.themoviedb.org/3/discover/movie?language={language}include_adult=false&with_genres={genre}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getTvByGenre(genre, language):
    url = f'https://api.themoviedb.org/3/discover/tv?language={language}&sort_by=popularity.desc&include_adult=false&with_genres={genre}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()