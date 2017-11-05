import os

class Config:
    '''
    General configuration parent class
    '''

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://khalid:pythonista@localhost/codeblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SIMPLEMDE_JS_IIFE = True
class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''



    DEBUG = True
config_options = {
'development':DevConfig,
'production':ProdConfig
}
