from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
list = Blueprint('list', __name__)


