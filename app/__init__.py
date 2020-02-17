from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Registering Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix = "/v1")
    return app