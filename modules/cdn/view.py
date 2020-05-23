from modules.course.models import Certificate
from modules.course.models import Homework
from modules.course.models import HomeworkSubmission
from modules.course.models import HomeworkEvaluation
from modules.course.models import SubSection

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


@cdn_blueprint.route('/homework/<hwork_id>', methods=["GET", "POST"])
@login_required
def homework(hwork_id):
    hwork = Homework.query.get(hwork_id)
    return send_from_directory('static/uploads/docs',
                           hwork.filename)

@cdn_blueprint.route('/homework/submitted/<submission_id>', methods=["GET", "POST"])
@login_required
def homework_submitted(submission_id):
    submission = HomeworkSubmission.query.get(submission_id)
    teacher_id = submission.sub_section.section.course.teacher_id
    if (current_user.id == submission.course_taker_id or 
        current_user.role == 'admin' or
        current_user.id == teacher_id
        ):
        return send_from_directory('static/uploads/homework_submits',
                           submission.filename)
    else:
        return 'No permission to view file'

@cdn_blueprint.route('/homework/evaluated/<evaluation_id>', methods=["GET", "POST"])
@login_required
def homework_evaluated(evaluation_id):
    evaluation = HomeworkEvaluation.query.get(evaluation_id)
    teacher_id = evaluation.sub_section.section.course.teacher_id
    if (current_user.id == evaluation.course_taker_id or 
        current_user.role == 'admin' or
        current_user.id == teacher_id
        ):
        return send_from_directory('static/uploads/homework_submits',
                           evaluation.filename)
    else:
        return 'No permission to view file'

