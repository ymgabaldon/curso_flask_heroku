""" Este archivo es el qeu se ocupa de lanzar la aplicación y está fuera del app
para ello importamos la función de la app que creaba la aplicación y que está en el __init__
Nos traemos también la db y para lanzar las tablas así como la clase User para la definción de usuarios"""

from app import create_app,db
from app.auth.models import User


if __name__ == '__main__':
    #Pasamos la configuración dev a la aplicación:
    #flask_app=create_app('dev')
    #Para producción utilizamos los parámetros de prod
    flask_app = create_app('prod')
    #Con esto creamos el aplicationcontext donde creamos la tablas por defecto si no existen.
    #Lo de los "contextos" es un poco lioso
    with flask_app.app_context():
        db.create_all()

        """Contrastamos si el usuario ya existe y si no, creamos uno"""
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@hogwarts.com', password='secret')
    #Y la lanzamos.
    flask_app.run()