# app\__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'  # Sirve para proteger de algún modo la sesión borrando las cookies
# y forzando al usuario a entrar y salir cada vez
bcrypt = Bcrypt()

"""Estos pasos están copiados del tutorial de udemy. Este es el init del raiz de la aplicación:
app\_init__.py"""

"""Indicar también que cada carpeta como auth o catalog son paquetes 'packages' que dice el profesor. Este init.py es 
el raíz que arrancará todo lo demás. Los paquetes aut y catalog cuelgan de app que es como lo hemos llamado. Además, 
existe una carpeta con configuración con tres posibilidades: dev, prod y test. """

db = SQLAlchemy()  # Como no hemos creado la aplicación de flask no podemos pasarla como arguemnto a SQLAlchemy
"""En este tipo de arquitecturas escalables, no se puede crear la app como en el ejemplo de hello flask de modo 
global y que esté disponible para todo el script sino que se crea dentro de una función a la que pasamos como 
argumento la configuración. De este modo, podemos pasar diferentes configuraciones a la app. Para eso, necesitamos 
pasar el camino de la localización o del archivo. Meto la lìnea seiguiente porque me da un error que no entiendo y en 
stackoverflow dicen que se arregla con un decorador y.... ¡¡funciona!! Bueno, en la lección siguiente lo añade y 
no aquí, sino en app/auth/models.py, con lo que lo quito de aquí."""


def create_app(config_type):  # config_type es dev,test o prod que están en la carpeta config
    app = Flask(__name__)
    # Aquí vamos a meter en la variable configuración el nombre del archivo que recibimos como argumento
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    # Ej: 'C:\\Users\\smgabaldon\\PycharmProjects\\book_catalog\\config\\dev.py'
    # Ahora tomamos la configuración para la aplicación del archivo (NOTA: Existe también form_envvariable):
    app.config.from_pyfile(configuration)
    # Finalmente, ya estamos listos para pasar la apliacación a la base de datos:
    db.init_app(app)
    bootstrap_bool = True  # Esta la pongo yo a pelo porque no hay manera de que me muestre los libros
    if bootstrap_bool:
        bootstrap.init_app(app)  # Pasamos igualmente el bootstrap a la aplicación

    login_manager.init_app(app)
    bcrypt.init_app(app)
    # Ahora el blueprint que no sé lo que es aun pero que hemos definido antes:
    from app.catalog import main  # Este main es como hemos llamado a la blueprint en el archivo app/catalog/__init__.py
    # app.catalog es porque está en el path app.catalog

    # En main está esto: main = Blueprint("main", __name__, template_folder='templates')
    # registramos la huella:
    app.register_blueprint(main)

    # Y también la huella para la autenticación:
    from app.auth import authentication
    app.register_blueprint(authentication)

    return app
