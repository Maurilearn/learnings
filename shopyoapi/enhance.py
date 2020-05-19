from flask_login import current_user
from modules.auth.models import User

def base_context():
    base_context = {
        'MESSAGE': '',
        'current_user': current_user,
        'User': User
    }
    return base_context.copy()
