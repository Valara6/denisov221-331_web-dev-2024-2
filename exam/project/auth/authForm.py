from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(message='Заполните поле Логин')])
    password = PasswordField('Password', validators=[DataRequired(message='Заполните поле пароля')])
    remember = BooleanField('Remember Me')
