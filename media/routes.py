from flask import Blueprint, jsonify, request, render_template
from media.utils import getExternal, getSimilar

media = Blueprint('media', __name__)

@media.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@media.route('/api/<string:type_media>/<string:media_id>/external_ids', methods=['GET'])
def getExternalMain(type_media, media_id):
    if type_media not in ['movie', 'tv']:
        return jsonify({'msg':'type_media should be movie or tv'})
    external = getExternal(type_media, media_id)
    return jsonify(external)

@media.route('/api/<string:type_media>/<string:media_id>/similar', methods=['GET'])
def getSimilarMain(type_media, media_id):
    if type_media not in ['movie', 'tv']:
        return jsonify({'msg':'type_media should be movie or tv'})

    language = request.args.get('language', 'en-US')
    
    similars = getSimilar(type_media, media_id, language)
    return jsonify(similars)