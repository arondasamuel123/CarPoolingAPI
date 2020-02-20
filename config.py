import os

class Config:
    """
    General configuration parent class
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SUPPRESS_SEND = False
    
class DevConfig(Config):
    """
    Development configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """
    DEBUG = True

class ProdConfig(Config):
    """
    Production configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig
}