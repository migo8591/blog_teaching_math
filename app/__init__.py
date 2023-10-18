from flask import Flask 
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from app.public import public_bp
from .extensions import db
migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    migrate = Migrate(app, db)
    ckeditor = CKEditor(app)
    app.register_blueprint(public_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app