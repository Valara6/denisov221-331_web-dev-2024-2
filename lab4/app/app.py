from flask import Flask, render_template, redirect, url_for, request, make_response, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required 
import hashlib
from my_sqldb import MyDb
import mysql.connector
import re

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = MyDb(app)

login_manager = LoginManager();

login_manager.init_app(app);

login_manager.login_view = 'login'
login_manager.login_message = 'Доступ к данной странице есть только у авторизованных пользователей '
login_manager.login_message_category = 'warning'

def get_roles():
    with db.connect().cursor(named_tuple=True) as cursor:
            query = ('SELECT * FROM roles')
            cursor.execute(query)
            roles = cursor.fetchall()
    return roles

class User(UserMixin):
    def __init__(self,user_id,user_login):
        self.id = user_id
        self.login = user_login
        

@login_manager.user_loader
def load_user(user_id):
    cursor= db.connect().cursor(named_tuple=True)
    query = ('SELECT * FROM users WHERE id=%s')
    cursor.execute(query,(user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
       return User(user.id,user.login)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        remember = request.form.get('remember')
        with db.connect().cursor(named_tuple=True) as cursor:
            query = ('SELECT * FROM users WHERE login=%s and password_hash=SHA2(%s,256) ')
            cursor.execute(query,(login, password))
            user_data = cursor.fetchone()
            if user_data:
                    login_user(User(user_data.id,user_data.login),remember=remember)
                    flash('Вы успешно прошли аутентификацию', 'success')
                    return redirect(url_for('index'))
        flash('Неверные логин или пароль', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/list_users')
def list_users():
    with db.connect().cursor(named_tuple=True) as cursor:
            query = ('SELECT * FROM users')
            cursor.execute(query)
            users = cursor.fetchall()
    return render_template('list_users.html', users = users)

def validate(field, value):
    errors={}
    allowed_password_chars="~!?@#$%^&*_-+()[]\{\}></\|.,:;\"]"
    allowed_lat_letters="abcdefghijklmnopqrstuvwxyz"
    allowed_kir_letters="абвгдежзийклмнопрстуфхцчшщъыьэюя"
    alloved_nums="1234567890"
    low_letters=allowed_lat_letters+allowed_kir_letters
    up_letters=low_letters.upper()
    allowed_password_letters=allowed_kir_letters+allowed_kir_letters.upper()+allowed_lat_letters+allowed_lat_letters.upper()
    allowed_login_letters=allowed_lat_letters+allowed_lat_letters.upper()
    allowed_login=alloved_nums+allowed_login_letters
    allowed_password=allowed_password_letters+alloved_nums+allowed_password_chars
    if field=="first_name":
        if not value:
            errors["Имя не может быть пустым"]="name_error"
    if field=="second_name":
        if not value:
            errors["Фамилия не может быть пустой"]="second_name_error"
    if field=="login":
        if not value:
            errors["Логин не может быть пустым"]="login_error"
        elif (any(ch not in allowed_login for ch in value)) or  len(value) < 5:
            errors["Логин должен состоять только из латинских букв и цифр и иметь длину не менее 5 символов"]="login_error"
            # Проверка пароля
    if field=="password":
        if not value:#+
            errors["Пароль не может быть пустым"]="password_error"
        elif not 8<=len(value)<=128:#+
            errors["Пароль должен иметь динну от 8 до 128 символов"]="password_error"
        elif not((any(ch in up_letters for ch in value)) and (any(ch in low_letters  for ch in value))):
            errors["Пароль должен содержать как минимум одну заглавную и одну строчную букву"]="password_error"
        elif (all(ch not in alloved_nums for ch in value)):#+
            errors["Пароль должен содержать как минимум одну цифру"]="password_error"
        elif re.search(" ", value):#+
            errors["Пароль должен быть без пробелов"]="password_error"
        #переделать не работает
        elif (any(ch not in allowed_password for ch in value)):
            errors['Пароль должен содержать только допустимые символы']="password_error"
    return errors

@app.route('/create_user', methods=['GET','POST'])
@login_required
def create_user():
    if request.method == "POST":
        first_name = request.form.get('name')
        second_name = request.form.get('lastname')
        middle_name = request.form.get('middlename')
        login = request.form.get('login')
        password = request.form.get('password')
        errors=validate("first_name",first_name)|validate("password",password)|validate("second_name",second_name)|validate("login",login)
        role_id = request.form.get('role')
        print(errors)
        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                if len(errors)!=0 :
                    return render_template("create_user.html", errors=errors)
                query = ('INSERT INTO users (login, password_hash, first_name, middle_name, last_name, role_id) values(%s, SHA2(%s,256), %s, %s, %s, %s) ')
                cursor.execute(query,(login, password, first_name, second_name, middle_name, role_id))
                db.connect().commit()
                flash('Вы успешно зарегестировали пользователя', 'success')
                return redirect(url_for('list_users'))
        except mysql.connector.errors.DatabaseError:
            db.connect().rollback()
            flash('Ошибка при регистрации', 'danger')
            
    roles = get_roles()
    return render_template('create_user.html', roles = roles)

@app.route('/show_user/<int:user_id>')
@login_required
def show_user(user_id):
    with db.connect().cursor(named_tuple=True) as cursor:
        query = ('SELECT users.*, roles.name as role_name FROM users LEFT JOIN roles ON users.role_id = roles.id WHERE users.id = %s')
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
    return render_template('show_user.html', user = user )


@app.route('/edit_user/<int:user_id>', methods=['GET','POST'])
@login_required
def edit_user(user_id):
    with db.connect().cursor(named_tuple=True) as cursor:
        query = ('SELECT users.*, roles.name as role_name FROM users LEFT JOIN roles ON users.role_id = roles.id WHERE users.id = %s')
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

    if request.method == "POST":
        first_name = request.form.get('name')
        second_name = request.form.get('lastname')
        middle_name = request.form.get('middlename')
        errors=validate("first_name",first_name)|validate("second_name",second_name)
        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                if len(errors)!=0 :
                     print(errors)
                     return render_template('edit_user.html', user = user,errors=errors)
                query = ('UPDATE users SET first_name=%s, middle_name=%s, last_name=%s where id=%s;')
                cursor.execute(query,(first_name,  second_name, middle_name, user_id))
                db.connect().commit()
                flash('Вы успешно обновили пользователя', 'success')
                return redirect(url_for('list_users'))
        except mysql.connector.errors.DatabaseError:
            db.connect().rollback()
            flash('Ошибка при обновлении', 'danger')
    return render_template('edit_password.html', user = user)

@app.route('/edit_password/<int:user_id>',methods=['GET',"POST"])
@login_required
def edit_password(user_id):
    with db.connect().cursor(named_tuple=True) as cursor:
        query = ('SELECT users.*, roles.name as role_name FROM users LEFT JOIN roles ON users.role_id = roles.id WHERE users.id = %s')
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
    if request.method == "POST":
        old_password=request.form.get('old_password')
        new_password=request.form.get('new_password')  
        repeat_new_password=request.form.get('repeat_new_password')
        errors=validate("password",new_password)
        print(old_password)
        print(user.password_hash==hashlib.sha256(old_password.encode()).hexdigest())
        print(hashlib.sha256(old_password.encode()).hexdigest())
        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                if hashlib.sha256(old_password.encode()).hexdigest()!=user.password_hash:
                    db.connect().rollback()
                    flash('Неверный пароль', 'danger')
                    return render_template('edit_password.html', user = user)
                if new_password!=repeat_new_password:
                    db.connect().rollback()
                    flash('Пароли не совпадают', 'danger')
                    return render_template('edit_password.html', user = user)
                if len(errors)!=0 :
                    print(errors)
                    flash('Ошибки в новом пароле', 'danger')
                    return render_template('edit_password.html', user = user,errors=errors)
                query = ('UPDATE users SET password_hash=SHA2(%s,256) where id=%s;')
                cursor.execute(query,(new_password, user_id))
                db.connect().commit()
                flash('Вы успешно обновили пароль пользователя', 'success')
                return redirect(url_for('list_users'))
        except:
            db.connect().rollback()
            flash('Ошибка при изменении пароля', 'danger')
    return render_template('edit_password.html', user = user)

@app.route('/delete_user/<int:user_id>', methods=["POST"])
@login_required
def delete_user(user_id): 
    with db.connect().cursor(named_tuple=True) as cursor:
        try:
            query = ('DELETE FROM users WHERE id=%s')
            cursor.execute(query, (user_id,))
            db.connect().commit()
            flash('Удаление успешно', 'success')
        except:
            db.connect().rollback()
            flash('Ошибка при удалении пользователя', 'danger')
    return redirect(url_for('list_users'))