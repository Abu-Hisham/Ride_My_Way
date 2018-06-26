import os


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aam786'
    DEBUG = False


class DevelopmentConfig(Config):

    """Configurations for development"""
    DEBUG = True


class TestingConfig(Config):

    """Configurations for Testing."""

    TESTING = True
    DEBUG = True


app_config = {
             'development':Config,
             'testing': TestingConfig
            }