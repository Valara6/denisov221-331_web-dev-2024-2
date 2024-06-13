import os

class MainConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    IMAGE_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'bookImages')
    DEBUG = True
    TEST = False


class MysqlConfig:
    MYSQL_HOST = 'std-mysql.ist.mospolytech.ru'
    MYSQL_USER = 'std_2484_exam'
    MYSQL_PASSWORD = '12345678'
    MYSQL_DATABASE = 'std_2484_exam'
