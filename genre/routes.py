from flask import Blueprint, jsonify
from flask import request 
import requests
from genre.utils import getGenreMovieList, getGenreTVList

genre = Blueprint('genre', __name__)

@genre.route('/api/genre/movie/list', methods=['GET'])
def getGenreListMovie():
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    genre_list = getGenreMovieList(language)
    return jsonify(genre_list)

@genre.route('/api/genre/tv/list', methods=['GET'])
def getGenreListTV():
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    genre_list = getGenreTVList(language)
    return jsonify(genre_list)

