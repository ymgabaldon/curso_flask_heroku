from flask_wtf import FlaskForm
# Importamos dos file types:
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User


# Vamos a crear una función que compruebe si el correo ya está en la base de datos. Se pueden crear funciones también
# para comprobar lo que se desee: usuarios, contraseñas, etc..:

def email_exists(form, field):
    """Recibe la instancia de registro de la clase registrationform creada en app.auth.models import User y el campo
    a comprobar, en este caso el email. Hacemos una query a la BBDD para ver si está. Hay que añadir esta función a
    las validaciones exigidas en la clase """
    email2 = User.query.filter_by(user_email=field.data).first()
    if email2:
        raise ValidationError("La dirección de correo ya existe")


# Para crear una form tenemos que crear una clase:

class RegistrationForm(FlaskForm):
    name = StringField("¿Cuál es tu nombre?",
                       validators=[DataRequired(), Length(3, 15, message='Entre 3 y 15 caracteres')])
    email = StringField("Escribe tu correo", validators=[DataRequired(), Email(), email_exists])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(5),
                                                       EqualTo('confirm', message="Deben coincidir las contraseñas")])
    confirm = PasswordField('Confirma tu contraseña', validators=[DataRequired()])
    submit = SubmitField("Registro")

    # Una vez creado el formulario de registro vemos en qué ruta lo desplegamos. para eso dentro de la estructura modular
    # se crea otro routes.`py


# Para el formulario de loging también hay que crear una clase:

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_loggedin = BooleanField('Permanecer conectado') #Los booleanfield meten checkbox
    submit = SubmitField('LogIn')
