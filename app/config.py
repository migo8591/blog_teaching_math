from dotenv import load_dotenv
from os.path import abspath, dirname, join
import os
load_dotenv()
# user = os.environ['MYSQL_USER']
# password = os.environ['MYSQL_PASSWORD']
# host = os.environ['MYSQL_HOST']
# database = os.environ['MYSQL_DATABASE']
myKeyword = os.environ['CLAVE']
DATABASE_CONNECTION_URI = os.environ['CONEXION']
PICK_UP = 'static/images/'

class Config:
    # Define the application directory
    # BASE_DIR = dirname(dirname(abspath(__file__)))
    # Media dir
    # MEDIA_DIR = join(BASE_DIR, 'media')
    # POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')
    UPLOAD_FOLDER =PICK_UP
    SECRET_KEY = myKeyword

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{database}"
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI
class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{database}"
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI
class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}