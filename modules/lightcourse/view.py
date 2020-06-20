
from modules.auth.access import roles_required

from modules.course.models import Grade

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask import current_app


from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user


from userapi.renders import render_md
from userapi.html import notify_danger
from userapi.html import notify_success
from userapi.html import notify_info
from userapi.html import notify_warning
from userapi.forms import flash_errors
from userapi.email import send_mail


from shopyoapi.enhance import base_context


from .forms import AddLightCourseForm

lightcourse_blueprint = Blueprint(
    "lightcourse",
    __name__,
    url_prefix='/lightcourse',
    template_folder="templates",
)


@lightcourse_blueprint.route("/")
def index():
    pass

@lightcourse_blueprint.route("/add")
@roles_required(['admin', 'teacher'])
@login_required
def add():
    context = base_context()
    form =  AddLightCourseForm()
    context['grades'] = Grade.query.all()
    return render_template('lightcourse/add.html', **context)
