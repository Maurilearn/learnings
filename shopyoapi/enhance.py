from flask_login import current_user
from modules.auth.models import User
from modules.school.models import Setting

from flask import current_app

def base_context():
    school_name = Setting.query.filter(
            Setting.name == 'school_name'
        ).first()
    contact_mail = Setting.query.filter(
            Setting.name == 'contact_mail'
        ).first()
    base_context = {
        'APP_NAME': current_app.config['APP_NAME'],
        'MESSAGE': '',
        'current_user': current_user,
        'User': User,
        'school_name': school_name.value,
        'contact_mail': contact_mail.value
    }
    return base_context.copy()
