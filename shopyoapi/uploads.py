
from werkzeug.security import generate_password_hash

from shopyoapi.init import db
from app import app

from modules.auth.models import User
from modules.school.models import Setting
# from modules.settings.models import Settings


def add_admin(name, email, password):
    with app.app_context():
        admin = User(
            name=name,
            email=email,
            role='admin'
        )
        admin.set_hash(password)
        admin.insert()
        print('[x] added admin:', name, email, password)
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

def add_setting(name, value):
    with app.app_context():
        s = Setting(
            name=name, 
            value=value)
        s.insert()
        print('[x] Added name:{} with value:{}'.format(name, value))