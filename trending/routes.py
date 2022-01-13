from flask import Blueprint, jsonify 
from trending.utils import getTrending
import trending

trending = Blueprint('trending', __name__)

@trending.route('/api/trending/<string:type>/<string:time_window>')
def getTrendingAllMain(type, time_window):
    if type not in ['all','movie','tv'] :
        return jsonify({'msg': 'incorrect type in request'})
    if time_window not in ['day','week']:
        return jsonify({'msg': 'incorrect time_window in request'})
    trending = getTrending(type, time_window)
    return jsonify(trending)