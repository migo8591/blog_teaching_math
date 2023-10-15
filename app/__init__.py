from flask import Flask 
from app.public import public_bp

app = Flask(__name__)
app.register_blueprint(public_bp)




def create_app(config):
    app.config.from_object(config)
    return app