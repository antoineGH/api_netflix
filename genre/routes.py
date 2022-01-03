from flask import Blueprint, jsonify
from flask import request 
from genre.utils import getGenreMediaList

genre = Blueprint('genre', __name__)

@genre.route('/api/genre/<string:type_media>/list', methods=['GET'])
def getGenreListMedia(type_media):
    if type_media not in ['movie', 'tv']:
        return jsonify({'message':'type_media should be movie or tv'})
    language = request.args.get('language', 'en-US')
    genre_list = getGenreMediaList(type_media, language)
    # print(genre_list['genres'])
    return jsonify(genre_list['genres'])