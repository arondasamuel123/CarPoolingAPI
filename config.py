import os

class Config:
    '''
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class DevConfig(Config):
    '''
    '''
    DEBUG = True

class ProdConfig(Config):
    '''
    '''
    
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig
}