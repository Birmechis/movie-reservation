from flask import Flask
from config import Config
from app.extension import db, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.movies import movie_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(movie_bp, url_prefix="/api/v1/")

    return app