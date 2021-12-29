from flask import Blueprint, jsonify, request
from find.utils import searchMedias, getDetails

find = Blueprint('find', __name__)

@find.route('/api/search/<string:type_media>', methods=['GET'])
def searchMovieMain(type_media):
    if type_media not in ['movie', 'tv']:
        return jsonify({'message':'type_media should be movie or tv'}), 404

    query = request.args.get('query', None)
    if not query:
        return jsonify({'message':'missing query in request'})

    medias = searchMedias(type_media, query)
    return jsonify(medias)

@find.route('/api/search/<string:type_media>/<int:media_id>', methods=['GET'])
def getDetailsMain(type_media, media_id):
    if type_media not in ['movie', 'tv']:
        return jsonify({'message':'type_media should be movie or tv'}), 404

    if not media_id:
        return jsonify({'message': 'missing media_id in request'}), 404

    movie = getDetails(type_media, media_id)
    return jsonify(movie)