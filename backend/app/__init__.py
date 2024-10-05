# backend/app/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .database import init_db

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    bcrypt.init_app(app)
    jwt.init_app(app)
    init_db(app)

    from .routes import auth, websites
    app.register_blueprint(auth.bp)
    app.register_blueprint(websites.bp)

    return app