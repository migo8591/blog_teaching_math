from flask import Flask 
from flask_ckeditor import CKEditor
from flask_login import LoginManager, current_user
from app.public.webforms import SearchForm
from app.public import public_bp
from app.auth import auth_bp
from app.admin import admin_bp
from .extensions import db
from flask_migrate import Migrate
from .models import Users
db 
migrate = Migrate()
def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(config)
        ckeditor = CKEditor(app)
        app.register_blueprint(public_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
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
        @app.route('/favicon.ico')
        def favicon():
            return app.send_static_file('images/favicon.ico')
        @app.context_processor
        def inject_user():
            user = current_user  # Obtiene el usuario actual si está autenticado
            return dict(user=user)  # Pasamos el usuario al contexto global
        @app.context_processor
        def base():
            form = SearchForm()
            return dict(form=form)
        return app

