from flask import current_app
import requests
import urllib.parse

from werkzeug.wrappers import response

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, response):
        response.headers["authorization"] = "Bearer " + self.token
        return response

def search_movie(query):
    encoded = urllib.parse.quote(query)
    url = f"https://api.themoviedb.org/3/search/movie?query={encoded}"
    print(url)
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def search_movie_id(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def get_genre_list(language):
    encoded = urllib.parse.quote(language)
    url = f'https://api.themoviedb.org/3/genre/movie/list?language={encoded}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

