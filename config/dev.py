"""Aquí metemos las variables de configuración o parámetros. Por ejemplo, las relativas a la base de datos:
Añadimos el debug=True
"""

DEBUG = True
SECRET_KEY = 'saruman'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:saruman@localhost/catalog_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False