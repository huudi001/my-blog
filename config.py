import os

class Config:
    '''
    general configuration
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    '''
    production configuration child class
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    '''
    development configuration child class
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://khalid:pythonista@localhost/mypersonal'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig         
}
