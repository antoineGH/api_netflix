from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
user = Blueprint('user', __name__)
