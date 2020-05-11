
from werkzeug.security import generate_password_hash

from shopyoapi.init import db
from app import app

from modules.auth.models import User
# from modules.settings.models import Settings


def add_admin(name, email, password, role):
    with app.app_context():
        admin = User(
            name=name,
            email=email,
            role=role
        )
        admin.set_hash(password)
        db.session.add(admin)
        db.session.commit()

'''
def add_setting(name, value):
    with app.app_context():
        if Settings.query.filter_by(setting=name).first():
            s = Settings.query.get(name)
            s.value = value
            db.session.commit()
        else:
            s = Settings(setting=name, value=value)
            db.session.add(s)
            db.session.commit()
'''