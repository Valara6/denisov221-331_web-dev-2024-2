from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def checkRights(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.UserRights(action):
                return func(*args, **kwargs) 
            flash("У вас нет доступа к данной странице. Пожалуйста, зайдите с аккаунта с такой привилегией", "warning")
            return redirect(url_for('auth.login'))
        return wrapper
    return decorator
