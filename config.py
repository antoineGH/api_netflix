# import json
import os 

# with open('config.json') as config_file:
#     config = json.load(config_file)

class Config:
    # SECRET_KEY = config.get('SECRET_KEY')
    # TMDB_BEARER = config.get('TMDB_BEARER')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    TMDB_BEARER = os.environ.get('TMDB_BEARER')
