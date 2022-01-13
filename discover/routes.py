from flask import Blueprint, jsonify
from flask import request 
from discover.utils import getDiscoverMedia

discover = Blueprint('discover', __name__)

accepted_sort = ['popularity.asc', 'popularity.desc', 'release_date.asc', 'release_date.desc',  'original_title.asc', 'original_title.desc', 'vote_average.asc', 'vote_average.desc']

@discover.route('/api/discover/<string:type_media>', methods=['GET'])
def getGenreListMovie(type_media):
    if type_media not in ['movie', 'tv']:
        return jsonify({'msg':'type_media should be movie or tv'})

    language = request.args.get('language', 'en-US')
    sort_by = request.args.get('sort_by', None)
    year = request.args.get('year', None)
    with_genres = request.args.get('with_genres', None)

    discover_movies = getDiscoverMedia(type_media, language, sort_by, year, with_genres)
    return jsonify(discover_movies)