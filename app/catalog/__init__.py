#app/config/__init__.py
from flask import Blueprint
"""Blueprint no es fácil de definir. Aquí se va a considerar como un conjunto de operaciones registradas en una aplicación
y sirve para simplificar grandes aplicaciones"""


"""Creamos una instancia y le pasamos el nombre como argumento, el __name__ **
y la carpeta donde se va a guardar que en este caso es el propio templates de config
**__name__ is just a convenient way to get the import name of the place the app is defined.
Flask uses the import name to know where to look up resources, templates, static files, instance folder, etc. 
When using a package, if you define your app in __init__.py then the __name__ will still point at the "correct" place relative
to where the resources are. ES decir, que el __name__ toma la referencia del camino de donde está el __init__.py
However, if you define it elsewhere, such as mypackage/app.py, then using __name__ would tell 
Flask to look for resources relative to mypackage.app instead of mypackage.
Y de la docu:
If you are using a single module (as in this example), you should use __name__ because
depending on if it’s started as application or imported as module the name will be different
 ('__main__' versus the actual import name).
 Vamos, que parece que está relacionado con el main, es decir, si es importado o el nombre con el que se importa para
 funcionar como módulo. Por otra parte, el template_folder que va a apuntar está dentro del catalog porque
  esta es la ruta desde donde buscará este init.py, porque está en catalog"""

main = Blueprint("main",__name__,template_folder='templates')

##Importamos las routes. Podríamos tenerlo todo junto pero el ejercicio va de separarlo todo.
"""Para evitar conflictos, se importa al final, no al principio. Aquí parece que está la clave. Todas las funciones que
están en routes son las que se publicarán en el navegador"""

from app.catalog import routes
