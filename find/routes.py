from flask import Blueprint, jsonify, request
from find.utils import searchMedias, getDetails

find = Blueprint('find', __name__)

@find.route('/api/search/<string:type_media>', methods=['GET'])
def searchMovieMain(type_media):
    if type_media not in ['movie', 'tv']:
        return jsonify({'msg':'type_media should be movie or tv'}), 404

    query = request.args.get('query', None)
    if not query:
        return jsonify({'msg':'missing query in request'})

    medias = searchMedias(type_media, query)
    return jsonify(medias)

@find.route('/api/search/<string:type_media>/<int:media_id>', methods=['GET'])
def getDetailsMain(type_media, media_id):
    if type_media not in ['movie', 'tv']:
        return jsonify({'msg':'type_media should be movie or tv'}), 404

    if not media_id:
        return jsonify({'msg': 'missing media_id in request'}), 404

    movie = getDetails(type_media, media_id)
    movie_light = dict({
        'id': movie['id'],
        'imdb_id': movie["imdb_id"],
        "genres": movie["genres"],
        "title": movie["title"],
        "original_language": movie["original_language"],
        "tagline": movie["tagline"],
        "homepage": movie["homepage"],
        "overview": movie["overview"],
        "runtime": movie["runtime"],
        "release_date": movie["release_date"],
        "production_countries": movie["production_countries"],
        "production_companies": movie["production_companies"],
        "poster_path": movie["poster_path"],
        "poster_full_path": "https://image.tmdb.org/t/p/w500/" + movie["poster_path"],
        "vote_average": movie["vote_average"],
        "vote_count": movie["vote_count"],
        "popularity": movie["popularity"],
        "video": movie["video"],
        "status": movie["status"],
        })
    return jsonify(movie_light)