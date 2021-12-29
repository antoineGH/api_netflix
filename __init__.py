from flask import Flask
from flask_cors import CORS
from config import Config

cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    from find.routes import find   
    from media.routes import media   
    from genre.routes import genre   
    from discover.routes import discover   
    from trending.routes import trending   
    from configuration.routes import configuration   
    from credit.routes import credit   
    app.register_blueprint(find)
    app.register_blueprint(media)
    app.register_blueprint(genre)
    app.register_blueprint(discover)
    app.register_blueprint(trending)
    app.register_blueprint(configuration)
    app.register_blueprint(credit)
    return app      

    