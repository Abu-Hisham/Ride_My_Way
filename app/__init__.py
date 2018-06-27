from flask import Flask
from app.auth import bp_auth
from app.main import bp_main

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(bp_auth, url_prefix="app/v1/auth")
    app.register_blueprint(bp_main, url_prefix="app/v1/main")
    return app
