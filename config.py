import datetime
import os 
import json

with open('config.json') as config_file:
    config = json.load(config_file)

class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_DATABASE')
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    # TMDB_BEARER = os.environ.get('TMDB_BEARER')
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    # JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = config.get('HEROKU_DATABASE')
    SECRET_KEY = config.get('SECRET_KEY')
    JWT_SECRET_KEY = config.get('JWT_SECRET_KEY')
    TMDB_BEARER = os.environ.get('TMDB_BEARER')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False