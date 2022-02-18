from flask import current_app
import requests
from auth.BearerAuth import BearerAuth

def getDiscoverMedia(type_media, language, sort_by, year, with_genres, page):
    if year:
        year= f'&year={year}'
    else:
        year= ''

    if with_genres:
        with_genres= f'&with_genres={with_genres}'
    else:
        with_genres= ''

    url = f'https://api.themoviedb.org/3/discover/{type_media}?language={language}&with_original_language={language[:2]}&sort_by={sort_by}{year}{with_genres}&include_adult=false&page={page}'
    response = requests.get(url, auth=BearerAuth(current_app.config['TMDB_BEARER']))
    return response.json()