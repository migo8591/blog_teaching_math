from dotenv import load_dotenv
import os
load_dotenv()
user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DATABASE']
myKeyword = os.environ['CLAVE']
DATABASE_CONNECTION_URI = os.environ['CONEXION']
class Config:
    SECRET_KEY = myKeyword

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{database}"
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{database}"
class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}