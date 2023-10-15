from flask import Flask 
from flask_ckeditor import CKEditor
from app.public import public_bp
from .extensions import db


def create_app(config):
    app = Flask(__name__)
    ckeditor = CKEditor(app)
    app.config.from_object(config)
    app.register_blueprint(public_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app