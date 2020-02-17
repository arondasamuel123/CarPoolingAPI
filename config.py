class Config:
    '''
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:123456@localhost/api'
    
class DevConfig(Config):
    '''
    '''
    

class ProdConfig(Config):
    '''
    '''
    
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig
}