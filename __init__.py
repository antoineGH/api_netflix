from flask import Flask
from flask_cors import CORS
from config import Config

cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    from movie.routes import movie   
    app.register_blueprint(movie)
    from genre.routes import genre   
    app.register_blueprint(genre)
    from discover.routes import discover   
    app.register_blueprint(discover)
    return app      

    