from modules.auth.forms import LoginForm
from modules.auth.models import User
from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.enhance import base_context


auth_blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix='/auth',
    template_folder="templates",
)

@auth_blueprint.route("/login")
def login():
    context = base_context()
    form = LoginForm()
    context['form'] = form
    return render_template('auth/login.html', **context)


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blueprint.route("/check_login", methods=['GET', 'POST'])
def check_login ():
    if request.method == 'POST':
        form = LoginForm()
        #message = ' '.join([form.email.data, form.password.data])
        #return render_template('auth/debug.html', message=message)
        #'''
        if form.validate_on_submit():
            user = User.query.filter(
                User.email == form.email.data
            ).first()

            if user is None or not user.check_hash(form.password.data):
                flash("please check your user id and password")
                return redirect(url_for("auth.login"))
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for("teacher.index"))
            elif user.role == 'teacher':
                return redirect(url_for("course.index"))
                
            else:
                return redirect(url_for("course.list"))
                
        else:
            return render_template('auth/login.html', form=form)
        #'''
    else:
        return 'Non browsable mode'

'''
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated():
               return current_app.login_manager.unauthorized()
            urole = current_app.login_manager.reload_user().get_urole()
            if ( (urole != role) and (role != "ANY")):
                return current_app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
'''