# Creamos este archivo com el último de todos. Importamos la blueprint
from app.catalog import main

# También hay que importar este archivo de rutas en el __init_ de catalog. Se cruzan los imports
"""Definimos una función y aquí es donde se supone que los blueprint funcionan, dado que lo utilizamos como 
decorador o algo parecido. En lugar de app.route referenciamos la app"""
""" De cara a poder mostrar las bases de datos en el navegador importamos lo necesario: las clases
que representan las tablas"""

from app.catalog.models import Book, Publication
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required

"""Para poder hacer operaciones CRUD importamos también la instancia de la base de datos:"""
from app import db
from app.catalog.forms import EditBookForm, CreateBookForm

# recordar que esto permite utilizar templates, htmls en este caso, para mejor presentación

"""Cuando lo escribíamos todo seguido, arrancábamos directamente la app como app = Flask(__name__) 
Ahora no podemos y utilizamos el blueprint como decorador para la ruta. Para la ejecución se necesita el run.py fuera de 
todo lo demás.
Lo que queramos mostrar se añade  como una función"""


@main.route('/')
# def hello():
#   return "Hola mundo"
def display_books():
    # Hacemos una query a la base de datos utilizando sqlalchemy. En este caso es un select all:
    books = Book.query.all()
    #  for book in books:
    #     print(book.title)
    return render_template('home.html', books=books)  # Pasamos la variable que contiene books al template
    # return render_template('home_antiguo.html', Books=books)  # Pasamos la variable que contiene books al template


""" Vamos ahora a hacer que funcionen los hiper´vinculos del publisher que hemos definido en ehome.html
Vemos que en este caso, en el blueprint creamos un camino nuevo que al final lleva la variable publisher_id
que entiendo que se rellenará con el valor que se indique en cada caso al hacer el clik"""


@main.route('/display/publisher/<publisher_id>')
def display_publisher(publisher_id):
    """La función recibe como argumento el id del publisher que queremos mostrar.
    Ahora una query que en la tabla de publicaciones se quede solo con el publisher que le digamos:"""

    publisher = Publication.query.filter_by(id=publisher_id).first()
    """Conseguido el filtro, vamos a hacer la query en la tabla de libros filtrando por este id"""
    publisher_books = Book.query.filter_by(pub_id=publisher.id).all()

    """Finalmente, lo sacamos con el html"""
    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)
    # return render_template('publisher_antiguo.html', publisher=publisher, publisher_books=publisher_books)


################OPERACIONES CRUD DESDE FORMULARIO#########################

@main.route('/book/delete/<book_id>', methods=['GET', 'POST'])
# Añadimos el decorador para obligar a que se necesite que el usuario esté logado:
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    ##Este es el libro a borrar. Comprobamos si es un método POST
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash("Libro eliminado con éxito")
        return redirect(url_for('main.display_books'))
    return render_template('delete_book.html', book=book, book_id=book_id)
"""Ahora el método para editar libros que también utiliza el decorador para el login y el formulario"""

@main.route('/edit/book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get(book_id)
    #Me ha parecido que al pasar el obj=book es capaz de heredar los campos qeu tiene el libro
    form = EditBookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.format = form.format.data
        book.num_pages = form.num_pages.data
        db.session.add(book)
        db.session.commit()
        flash('Book Edited Successfully')
        return redirect(url_for('main.display_books'))
    return render_template('edit_book.html', form=form)
"""Método para crear nuevos registros"""

@main.route('/create/book/<pub_id>', methods=['GET', 'POST'])
@login_required
def create_book(pub_id):
    form = CreateBookForm()
    form.pub_id.data = pub_id  # pre-populates pub_id
    """Como siempre, comprobamos si es un POST y estamos logados (entramos en el if) o es un GET y vamos al otro 
    return. El GET se obtiene siempre cuando accedemos por primera vez a la modificación y el POST cuando remitimos los 
    resultados o el nuevo refistro, en este caso"""
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, avg_rating=form.avg_rating.data,
                    book_format=form.format.data, image=form.img_url.data, num_pages=form.num_pages.data,
                    pub_id=form.pub_id.data)
        db.session.add(book)
        db.session.commit()
        flash('Libro añadido correctamente')
        return redirect(url_for('main.display_publisher', publisher_id=pub_id))
    return render_template('create_book.html', form=form, pub_id=pub_id)

@main.route('/prueba')
def funcion2():
    return "Esto es una prueba"
