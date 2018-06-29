from flask import Flask

import instance
from app.auth import bp_auth
from app.main import bp_main

from instance.config import app_config
from app.main import models,routes


def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(instance.config)
    app.config.from_pyfile('config.py')
    app.register_blueprint(bp_auth, url_prefix="/app/v1/auth/")
    app.register_blueprint(bp_main, url_prefix="/app/v1/main/")
    return app

