from flask import Flask 
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from app.public import public_bp
from app.auth import auth_bp
from .extensions import db
from .models import Users

migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    migrate = Migrate(app, db)
    ckeditor = CKEditor(app)
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    @app.context_processor
    def inject_user():
        user = current_user  # Obtiene el usuario actual si está autenticado
        return dict(user=user)  # Pasamos el usuario al contexto global
    return app

