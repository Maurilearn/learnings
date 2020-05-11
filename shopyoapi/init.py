from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from faker import Faker
from flask_uploads import UploadSet, IMAGES

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
fake = Faker()

photos = UploadSet('photos', IMAGES)
