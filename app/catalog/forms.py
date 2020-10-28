# app\catalog\forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired

"""Formulario para ecitar un libro. Estos son los campos que se pueden editar. Tiene que heredar la clase flaskform"""
class EditBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    format = StringField('Format', validators=[DataRequired()])
    num_pages = StringField('Pages', validators=[DataRequired()])
    submit = SubmitField('Update')

    """Formulario para crear un nuevo libro"""



class CreateBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    avg_rating = FloatField('Rating', validators=[DataRequired()])
    format = StringField('Format', validators=[DataRequired()])
    img_url = StringField('Image', validators=[DataRequired()])
    num_pages = IntegerField('Pages', validators=[DataRequired()])
    pub_id = IntegerField('PublisherID', validators=[DataRequired()])
    submit = SubmitField('Create')