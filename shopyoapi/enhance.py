from flask_login import current_user
from modules.auth.models import User
from flask import current_app

def base_context():
    base_context = {
        'APP_NAME': current_app.config['APP_NAME'],
        'MESSAGE': '',
        'current_user': current_user,
        'User': User
    }
    return base_context.copy()
