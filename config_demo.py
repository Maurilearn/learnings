import os
import json
import sys
from flask import url_for

from userapi.html import notify_warning

base_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_path, 'config.json')) as f:
    json_info = json.load(f)

def check_environ(env_var_name):
    if env_var_name in  os.environ:
        return os.environ[env_var_name]
    else:
        print('[DANGER] Environment variable not found:', env_var_name)
        print('    try a opening a different **system** shell or make sure it is set')
        sys.exit()


class Config:
    """Parent configuration class."""
    APP_NAME = 'Maurilearn'

    DEBUG = False
    # "mysql://username:password@localhost/db_name"
    # pip install pymysqldb
    SQLALCHEMY_DATABASE_URI = '' # we override it below
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "qow32ijjdkc756osk5dmck"  # Need a generator

    LOGIN_VIEW = "auth.login"
    LOGIN_MESSAGE = notify_warning("Please login for access")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB

    BASE_DIR = base_path
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

    UPLOAD_VIDEO_FOLDER = os.path.join(STATIC_DIR, 'uploads/video')
    UPLOAD_CERTIFICATES_FOLDER = os.path.join(STATIC_DIR, 'certificates')
    UPLOADED_PHOTOS_DEST = os.path.join(STATIC_DIR, 'uploads/img')
    UPLOADED_PHOTOS_ALLOW = ('png', 'jpg', 'jpeg')
    UPLOADED_DOCS_DEST = os.path.join(STATIC_DIR, 'uploads/homeworks') # must change to homework
    UPLOADED_DOCS_ALLOW = ('pdf', 'docx', 'odt')
    UPLOADED_ALLDOCS_DEST = os.path.join(STATIC_DIR, 'uploads/alldocs')
    UPLOADED_ALLDOCS_ALLOW = ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 
        'docx', 'xls', 'xlsx', 'ppt', 'pdf')
    UPLOADED_HOMEWORKSUBMITS_DEST = os.path.join(STATIC_DIR, 'uploads/homework_submits')
    UPLOADED_HOMEWORKSUBMITS_ALLOW = ('pdf', 'docx', 'odt')

    SMTP_HOST = ''
    SMTP_PORT = 458
    SMTP_MAIN_MAIL = ''
    SMTP_PASS = ''

    DEFAULT_PASS_ALL = 'pass'
    LIGHTCOURSE_QUIZ_NUM = 2
    SCHOOL_DEFAULTS = os.path.join(STATIC_DIR, 'default')


class DevelopmentConfig(Config):
    """Configurations for development"""

    # SMTP_HOST = 'localhost'
    # SMTP_PORT = 1025
    # SMTP_MAIN_MAIL = 'dev@maurilearn.com'

    ENV = "development"
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(base_path, 'amilearn.db'))
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{server_name}/{db_name}".format(
            username='root',
            password=check_environ('AMILEARN_MYSQL_PASS'),
            server_name='localhost',
            db_name='amilearn'
        )
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_MAIN_MAIL = 'arj.message@gmail.com'
    SMTP_PASS = check_environ('AMILEARN_MAIL_PASS')


class TestingConfig(Config):
    """Configurations for testing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    SMTP_HOST = ''
    SMTP_PORT = 458
    SMTP_MAIN_MAIL = ''
    SMTP_PASS = ''


class PythonAnywhere(Config):
    """Configurations for testing"""

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{server_name}/{db_name}".format(
            username='root',
            password=check_environ('AMILEARN_MYSQL_PASS'),
            server_name='localhost',
            db_name='amilearn'
        )
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_MAIN_MAIL = 'arj.message@gmail.com'
    SMTP_PASS = ''


app_config = {
    "development": DevelopmentConfig,
    "production": Config,
    "testing": TestingConfig,
    "pythonanywhere": PythonAnywhere
}
