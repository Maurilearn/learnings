
from modules.auth.models import User
from modules.course.models import Certificate
from modules.course.models import Course
from modules.lightcourse.models import LightCertificate
from modules.lightcourse.models import LightCourse

from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from shopyoapi.enhance import base_context


profile_blueprint = Blueprint(
    "profile",
    __name__,
    url_prefix='/profile',
    template_folder="templates",
)


@profile_blueprint.route("/<user_id>")
@login_required
def index(user_id):
    context = base_context()
    user = User.query.get(user_id)
    context['user'] = user
    context['num_enrolled'] = len(user.courses) + len(user.light_courses)
    finished = Certificate.query.filter(
            Certificate.course_taker_id == user.id
        ).all()
    light_finished = LightCertificate.query.filter(
            LightCertificate.course_taker_id == user.id
        ).all()
    context['num_completed'] = len(finished) + len(light_finished)
    num_available = len(Course.query.all()) + len(LightCourse.query.all())
    if current_user.role == 'student':
        context['num_available_specific'] = len(Course.query.filter(
                Course.grade_id == current_user.grade_id
            ).all()) + len(
                LightCourse.query.filter(
                    LightCourse.grade_id==current_user.grade_id
                    ).all()
            )
    context['num_available'] = num_available
    return render_template('profile/index.html', **context)
