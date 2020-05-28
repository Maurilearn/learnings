class Config:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "qow32ijjdkc756osk5dmck"  # Need a generator
    HOMEPAGE_URL = "/course"
    LOGIN_VIEW = "auth.login"
    LOGIN_MESSAGE = "Please login for access"

    UPLOADED_PHOTOS_DEST = 'static/img' 
    UPLOADED_PHOTOS_ALLOW = ('png', 'jpg', 'jpeg')
    UPLOADED_DOCS_DEST = 'static/uploads/docs' 
    UPLOADED_DOCS_ALLOW = ('pdf', 'docx', 'odt')
    UPLOADED_HOMEWORKSUBMITS_DEST = 'static/uploads/homework_submits' 
    UPLOADED_HOMEWORKSUBMITS_ALLOW = ('pdf', 'docx', 'odt')

    SMTP_HOST = ''
    SMTP_PORT = 458
    SMTP_MAIN_MAIL = ''
    SMTP_PASS = ''


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
    SMTP_PASS = 'berry654321'


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
