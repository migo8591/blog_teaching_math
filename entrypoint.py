from app import create_app
from app.config import config


configuracion1= config['development']
configuracion2 = config['production']
configuracion3 = config['testing']

myApp=create_app(configuracion1)

if __name__ == '__main__':
    myApp.run()