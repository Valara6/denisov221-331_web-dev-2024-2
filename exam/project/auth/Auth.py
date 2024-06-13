# Import necessary modules
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from project.run import app, db
from flask import Blueprint, request, flash, render_template, redirect, url_for
from project.auth.user import User
from project.auth.authForm import LoginForm

# Initialize the Blueprint
auth = Blueprint('auth', __name__)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'У вас недостаточно прав для выполнения данного действия'
login_manager.login_message_category = 'danger'

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    user = db.ExecuteQuery("SELECT * FROM users WHERE id = %s ", [user_id])
    if user is not None:
        return User(user[0].id, user[0].login, user[0].first_name, user[0].last_name, user[0].second_name, user[0].role)
    return None


# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form2 = LoginForm()
    if form2.validate_on_submit():
        user = db.ExecuteQuery("select * from users where login = %s and password_hash = SHA2(%s ,256)",
                               [form2.login.data, form2.password.data], query_type="get")
        if user != []:
            print(user)
            userobject = User(user[0].id, user[0].login, user[0].first_name, user[0].last_name, user[0].second_name, user[0].role)
            login_user(userobject, remember=form2.remember.data)
            return redirect(url_for('index'))
        else:
            flash("Невозможно аутентифицироваться с указанными логином и паролем", "danger")
    return render_template("auth/login.html", form=form2)


# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
