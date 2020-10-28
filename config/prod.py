"""ACambiamos los datos para el despliegue en heroku
"""

DEBUG = False
SECRET_KEY = 'saruman'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:saruman@localhost/catalog_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False