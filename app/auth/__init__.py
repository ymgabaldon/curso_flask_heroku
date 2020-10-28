# app/auth/init.py
from flask import Blueprint

authentication = Blueprint('authentication', __name__, template_folder='templates')
# Como en el caso anterior, hay un import cruzado, dado que aquí se importan las rutas y allí los blueprint
from app.auth import routes
