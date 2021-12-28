from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getCountries():
    url = f'https://api.themoviedb.org/3/configuration/countries'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getLanguages():
    url = f'https://api.themoviedb.org/3/configuration/languages'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()

def getTimezones():
    url = f'https://api.themoviedb.org/3/configuration/timezones'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()