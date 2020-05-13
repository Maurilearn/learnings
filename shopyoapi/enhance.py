from flask_login import current_user

def base_context():
    base_context = {
        'MESSAGE': '',
        'current_user': current_user
    }
    return base_context.copy()
