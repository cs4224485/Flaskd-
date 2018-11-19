# Author: harry.cai
# DATE: 2018/9/2

from flask import Flask
from .views import auth
from .views import index
from flask_session import Session
import settings


def create_app():
    app = Flask(__name__)
    app.register_blueprint(index.main)
    app.register_blueprint(auth.authenticate)
    app.config.from_object(settings.DefaultConfig)
    Session(app)

    return app

