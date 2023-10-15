from flask import Flask 
from flask_ckeditor import CKEditor
from app.public import public_bp
from .extensions import db
from config import DATABASE_CONNECTION_URI


app = Flask(__name__)
ckeditor = CKEditor(app)
app.register_blueprint(public_bp)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
db.init_app(app)
with app.app_context():
    db.create_all()



def create_app(config):
    app.config.from_object(config)
    return app