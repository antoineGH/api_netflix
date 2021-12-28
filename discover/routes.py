from flask import Blueprint, jsonify
from flask import request 
import requests
from discover.utils import getMovieByGenre, getTvByGenre

discover = Blueprint('discover', __name__)

# @discover.route('/api/discover/movie', methods=['GET'])
# def getGenreListMovie():
#     if 'language' in request.args:
#         language = requests.args.get('language')
#     else:
#         language='en-US'
#     genre_list = getGenreMovieList(language)
#     return jsonify(genre_list)

# @discover.route('/api/discover/tv', methods=['GET'])
# def getGenreListTV():
#     if 'language' in request.args:
#         language = requests.args.get('language')
#     else:
#         language='en-US'
#     genre_list = getGenreTVList(language)
#     return jsonify(genre_list)

@discover.route('/api/discover/movie/genre', methods=['GET'])
def getMovieByGenreMain():
    if 'genre' not in request.args:
        return jsonify({'message': 'missing genre_id in request'})
    genre = request.args.get('genre')
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    movie_list = getMovieByGenre(genre, language)
    return jsonify(movie_list)

@discover.route('/api/discover/tv/genre', methods=['GET'])
def getTvByGenreMain():
    if 'genre' not in request.args:
        return jsonify({'message': 'missing genre_id in request'})
    genre = request.args.get('genre')
    if 'language' in request.args:
        language = requests.args.get('language')
    else:
        language='en-US'
    tv_list = getTvByGenre(genre, language)
    return jsonify(tv_list)

# sort_by - string - popularity.asc, popularity.desc, release_date.asc, release_date.desc, revenue.asc, revenue.desc, primary_release_date.asc, primary_release_date.desc, original_title.asc, original_title.desc, vote_average.asc, vote_average.desc, vote_count.asc, vote_count.desc
# page - integer - Specify the page of results to query. - minimum: 1 maximum: 1000 default: 1
# language - string - Specify a language to query translatable fields with. ([a-z]{2})-([A-Z]{2})
# with_genres - string - Comma separated value of genre ids that you want to include in the results.
# year - integer - A filter to limit the results to a specific year (looking at all release dates).
# include_adult - boolean - A filter and include or exclude adult movies.