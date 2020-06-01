import os
import json

with open('config.json') as f:
    json_info = json.load(f)

class Config:
    """Parent configuration class."""
    APP_NAME = 'Amilearn'

    DEBUG = False
    # "mysql://username:password@localhost/db_name"
    # pip install pymysqldb
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{name}/{db_name}".format(
            username=json_info['connect']['username'],
            password=os.environ['AMILEARN_MYSQL_PASS'],
            name=json_info['connect']['name'],
            db_name=json_info['connect']['db_name']
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "qow32ijjdkc756osk5dmck"  # Need a generator
    HOMEPAGE_URL = "/course"
    LOGIN_VIEW = "auth.login"
    LOGIN_MESSAGE = "Please login for access"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB

    UPLOAD_VIDEO_FOLDER = 'static/uploads/video' 
    UPLOADED_PHOTOS_DEST = 'static/img' 
    UPLOADED_PHOTOS_ALLOW = ('png', 'jpg', 'jpeg')
    UPLOADED_DOCS_DEST = 'static/uploads/docs' 
    UPLOADED_DOCS_ALLOW = ('pdf', 'docx', 'odt')
    UPLOADED_HOMEWORKSUBMITS_DEST = 'static/uploads/homework_submits' 
    UPLOADED_HOMEWORKSUBMITS_ALLOW = ('pdf', 'docx', 'odt')

    SMTP_HOST = ''
    SMTP_PORT = 458
    SMTP_MAIN_MAIL = ''
    SMTP_PASS = os.environ['AMILEARN_MAIL_PASS']


class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True
    # SMTP_HOST = 'localhost'
    # SMTP_PORT = 1025
    # SMTP_MAIN_MAIL = 'dev@maurilearn.com'
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_MAIN_MAIL = 'arj.message@gmail.com'
    SMTP_PASS = os.environ['AMILEARN_MAIL_PASS']


class TestingConfig(Config):
    """Configurations for testsing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    SMTP_HOST = ''
    SMTP_PORT = 458
    SMTP_MAIN_MAIL = ''
    SMTP_PASS = ''


app_config = {
    "development": DevelopmentConfig,
    "production": Config,
    "testing": TestingConfig,
}
