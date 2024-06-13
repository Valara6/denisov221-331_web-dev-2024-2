from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed
from project.run import db


import datetime

year = datetime.datetime.now().year
msg = "Это обязательное поле. Пожалуйста заполните"
msg2 = "Файл должен быть изображением (jpg, jpeg, png и тд)"

limitmsg = "Дата не может быть меньше 1990 и больше {}".format(year)

class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired(message=msg)])
    description = TextAreaField('Описание книги', validators=[DataRequired(message=msg)])
    year = IntegerField('Год выпуска', validators=[DataRequired(message=msg), NumberRange(min=1990, max=year, message=limitmsg)])
    publisher = StringField('Издательство', validators=[DataRequired(message=msg)])
    author = StringField('Автор книги', validators=[DataRequired(message=msg)])
    pages = IntegerField('Количество страниц', validators=[DataRequired(message=msg)])
    genres = SelectMultipleField('Жанры', coerce=int, choices=[], validate_choice=False, validators=[DataRequired(message=msg)])
    cover = FileField('Обложка', validators=[DataRequired(message=msg2)])
