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
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/'
    UPLOADED_PHOTOS_ALLOW = ('png', 'jpg', 'jpeg')


class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """Configurations for testsing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True


app_config = {
    "development": DevelopmentConfig,
    "production": Config,
    "testing": TestingConfig,
}
