
from flask_login import current_user
from flask import current_app
from flask import redirect
from flask import url_for

from functools import wraps

def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            #if not current_user.is_authenticated():
            #   return current_app.login_manager.unauthorized()
            #urole = current_app.login_manager.reload_user().get_urole()
            # if ( (urole != role) and (role != "ANY")):
            if not current_user.role in roles:
                # return current_app.login_manager.unauthorized()
                return redirect(url_for('auth.login'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper