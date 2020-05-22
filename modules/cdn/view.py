from modules.course.models import Certificate

from flask import Blueprint
from flask import send_from_directory
from flask_login import login_required
from flask_login import current_user

cdn_blueprint = Blueprint(
    "cdn",
    __name__,
    url_prefix='/cdn',
    template_folder="templates",
)


@cdn_blueprint.route("/")
@login_required
def index():
    pass


@cdn_blueprint.route('/certificate/<course_id>', methods=["GET", "POST"])
@login_required
def certificate(course_id):
    # app.config['UPLOAD_FOLDER']
    certif = Certificate.query.filter(
        (Certificate.course_taker_id == current_user.id) &
        (Certificate.course_id == course_id)
        ).first() # course completed
    if certif:
        return send_from_directory('static/certificates',
                           certif.filename)
    else:
        return "You can't view this certificate"


