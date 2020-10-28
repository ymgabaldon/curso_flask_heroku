from app.auth import authentication as at
from flask import render_template, request, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user


# El decorador para las rutas va asociado a la blueprint

@at.route('/register', methods=['GET', 'POST'])
def register_user():
    """Metemos un control para que en caso de que el usuario ya esté logado no pueda ir a las páginas de register o
    de login. Para eso se utiliza current_user:"""
    if current_user.is_authenticated:
        flash(("Ya estás dentro de la aplicación"))
        return redirect(url_for('main.display_books'))

    # Inicializamos a none los datos de entrada (en una fase posterior los elimina):
    # name=None
    # email=None

    form = RegistrationForm()
    # Si el método es post, es decir, va a capturar los valores, se rellenan las variables:
    #   if request.method == 'POST':
    #       name = form.name.data
    #       email = form.name.data

    # Si la petición es un GET, simplemente sacamos por pantalla el formulario
    # El Post permite al usuario meter los datos. Tenemos que crear el código para esto. Antes lo hicimos con el
    # if request.method=='POST'. Ahora utilizamos esto que comprueba 1: es un post request, 2: valida los datos de acuerdo
    # con los validators que hemos definido en nuestra clase form
    if form.validate_on_submit():
        """Utilizamos la función create_user de la clase User de models pasándole los parámetros que ha escrito el 
        usuario """
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash("Registro completado con éxito")
        """Una vez completado el registro le mandamos a una de las páginas. PAra ello lso métodos redirect y url_for
        con la blueprint, en este caso a la página de login. Se pone el authentication en lugar del at, no sé por qué
        Si no se hace así, da error"""
        return redirect((url_for('authentication.login_user')))
    """Si no se cumple, entonces lo mandamos de nuevo al formulario que se despliega con el GET."""

    return render_template('registration.html', form=form)

    # Lo referenciamos a la carpeta template con el nombre registration. pasamos las variables name y email al render
    # template para que aparezcan en el navegador return render_template('registration.html',form=form,name=name,
    # email=email)


""" Creamos la ruta login a la que reenviamos en el return anterior con el redirect. Cambiamos el nombre de la función
para que no entre en conflicto con la que hemos creado en modesl"""


@at.route('/login', methods=['GET', 'POST'])
def do_the_login():
    """Metemos un control para que en caso de que el usuario ya esté logado no pueda ir a las páginas de register o
    de login. Para eso se utiliza current_user:"""
    if current_user.is_authenticated:
        flash(("Ya estás dentro de la aplicación"))
        return redirect(url_for('main.display_books'))

    """ Creamos una instancia de la clase LoginForm que hemos definido en forms.py"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            flash('Invalid Credentials, Please try again')
            return redirect(url_for('authentication.do_the_login'))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.display_books'))
    # Si es un get simplemente devolvemos el formulario de entrada
    return render_template('login.html', form=form)


"""Ahora definimos el log out. Es lo más sencillo. Simplemente se invoca un método que borra al usuario de la sesión.
Se le tiene que pasar al método como decorador el hecho de estar logado. Esto se hace con login_required"""


@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    """Lo enviamos a la página de origen"""
    return redirect(url_for('main.display_books'))


"""Para gestionar el error 404 de escribir mal una url, solo se necesita una función que puede ir por ejempelo aquí y 
el correspondiente template. Para indicar que es la función de gestión de errores, se pone app_errohandler en el decora
dor"""


@at.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
