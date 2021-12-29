from flask import Blueprint, jsonify, request
from credit.utils import getCredits, getCreditID

credit = Blueprint('credit', __name__)

@credit.route('/api/<string:type_media>/<string:media_id>/credits', methods=['GET'])
def getCreditIDMain(type_media, media_id):
    if type_media not in ['movie', 'tv']:
        return jsonify({'message':'type_media should be movie or tv'})

    creditID = getCreditID(type_media, media_id)
    return jsonify(creditID)

@credit.route('/api/credit', methods=['GET'])
def getCreditsMain():
    credit_id = request.args.get('credit_id', None)
    if not credit_id:
        return jsonify({'message': 'missing credit_id in request'}), 404
    credit = getCredits(credit_id)
    return jsonify(credit)
