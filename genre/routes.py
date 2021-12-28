from flask import Blueprint, jsonify
from flask import request 
import requests
from genre.utils import getGenreList

genre = Blueprint('genre', __name__)

@genre.route('/api/genre/movie/list', methods=['GET'])
def getGenreListMain():
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    genre_list = getGenreList(language)
    return jsonify(genre_list)

