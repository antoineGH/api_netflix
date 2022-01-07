from flask import Flask
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    with app.test_request_context():
        from models import Account, User, List, Movie
        db.create_all()
        
    from find.routes import find   
    from media.routes import media   
    from genre.routes import genre   
    from discover.routes import discover   
    from trending.routes import trending   
    from configuration.routes import configuration   
    from credit.routes import credit   
    from account.routes import account   
    from user.routes import user   
    from list.routes import list   
    from movie.routes import movie   
    
    app.register_blueprint(find)
    app.register_blueprint(media)
    app.register_blueprint(genre)
    app.register_blueprint(discover)
    app.register_blueprint(trending)
    app.register_blueprint(configuration)
    app.register_blueprint(credit)
    app.register_blueprint(account)
    # app.register_blueprint(user)
    # app.register_blueprint(list)
    app.register_blueprint(movie)
    return app      

    