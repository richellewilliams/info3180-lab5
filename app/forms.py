from flask_wtf import FlaskFrom
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class MovieForm(FlaskFrom):
    title = StringField('Movie Title', validators=[InputRequired()])
    decription = TextAreaField('Description', validators=[InputRequired()])
    poster = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Only Images Allowed!')])