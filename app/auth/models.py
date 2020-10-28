# auth/models.py
# python code creating a user

from datetime import datetime
from app import db, bcrypt  # app/__init__.py
from app import login_manager
from flask_login import UserMixin

"""Vamos a crear una tabla con usuarios, para lo cual se necesita una clase que herede db.Model que es un objeto de SQLAlchemy
que se creó en app__init__,py"""


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    """Función para desencriptar el password"""

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    """Las classmethod son métodos asociados a la clase, no a una instancia de la misma, por loq ue para invocarlos no 
      se requiere una instancia, sino que se pueden crear directamente. El argumento cls es el equivalente a self para este
      tipo de clases"""

    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'))

        db.session.add(user)  # Con este lo añadimos a la bd
        db.session.commit()  # Y persistimos la tabla con el commit

        return user


"""Parece que el user_loader devuelve un objeto user o none si no existe y es el modo que tiene flask de manejar los
usuarios que se logan a la aplicación. Almacena el id en la sesión activa así como impide que solo accedan a la página
usuarios logados"""


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
