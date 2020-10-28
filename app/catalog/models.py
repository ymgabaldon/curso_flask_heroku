### Vamos a meter aquí toda la creación de tablas, etc... Para ello nos traemos la instancia db de app:

from app import db
from datetime import datetime


### Ahora copiamos las clases de creación de las tablas. Copiamos directamente las que suamos en hello flask
### Además, tenemos que añadir la creación de las tablas dentro del run.py. antes lo hacíamos al vuelo en el único
### archivo que se ejecutaba. En python, para crear las clases utilizamos clases en lugar de sql tradicional


class Publication(db.Model):
    __tablename__ = 'publication'  # Definimos el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)  # Pasamos el nombre de la columna
    name = db.Column(db.String(80), nullable=False)  # Y de la otra

    def __init__(self, name):
        # self.id = id en versiones posteriores quita el id porque al ser primary key es más fácil que se genere automáticamente
        self.name = name

    def __repr__(self):
        # return 'The id is {}, Name is is {}'.format(self.i

        return 'The Name is {}'.format(self.name)


# BOOK TABLE

""" Añado directamente la tabla "book" directamente desde el repo en el mismo código.
Se puede ver que el proceso de creación es el mismo y los pasos similares.
"""


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)  # Con index =True se crea un índice asociado al campo
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)  # con unique = True se obliga a que no haya duplicados.
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())  # Pasamos como valor por defecto la fecha de hoy

    # ESTABLISH A RELATIONSHIP BETWEEN PUBLICATION AND BOOK TABLES
    """ Aquí se crea la relación 1- n entre la tabla publication y su clave id y esta columna
    Por este motivo, se define como una clave foránea
    """
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
