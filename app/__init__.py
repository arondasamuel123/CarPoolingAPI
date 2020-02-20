from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config_options

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    # Initializing Extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Registering Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix = "/v1")
    return app