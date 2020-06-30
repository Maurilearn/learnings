from modules.course.models import Certificate
from modules.course.models import Homework
from modules.course.models import HomeworkSubmission
from modules.course.models import HomeworkEvaluation
from modules.course.models import SubSection
from modules.course.models import Resource

from modules.lightcourse.models import LightResource
from modules.lightcourse.models import LightHomework
from modules.lightcourse.models import LightHomeworkSubmission
from modules.lightcourse.models import LightHomeworkEvaluation
from modules.lightcourse.models import LightCertificate 

from modules.school.models import Setting

from flask import Blueprint
from flask import send_from_directory
from flask import current_app
from flask import flash

from flask_login import login_required
from flask_login import current_user
from userapi.html import notify_info


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
        # '''
        return send_from_directory(current_app.config['UPLOAD_CERTIFICATES_FOLDER'],
                           certif.filename)
        # '''
        '''
        return '{}<br>{}'.format(current_app.config['UPLOAD_CERTIFICATES_FOLDER'],
            certif.filename)
            '''
    else:
        return "You can't view this certificate"


@cdn_blueprint.route('/homework/<hwork_id>', methods=["GET", "POST"])
@login_required
def homework(hwork_id):
    hwork = Homework.query.get(hwork_id)
    return send_from_directory(current_app.config['UPLOADED_DOCS_DEST'],
                           hwork.filename, 
                           as_attachment=True)

@cdn_blueprint.route('/homework/submitted/<submission_id>', methods=["GET", "POST"])
@login_required
def homework_submitted(submission_id):
    submission = HomeworkSubmission.query.get(submission_id)
    teacher_id = submission.sub_section.section.course.teacher_id
    if (current_user.id == submission.course_taker_id or 
        current_user.role == 'admin' or
        current_user.id == teacher_id
        ):
        return send_from_directory(current_app.config['UPLOADED_HOMEWORKSUBMITS_DEST'],
                           submission.filename, 
                           as_attachment=True)
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
        return send_from_directory(current_app.config['UPLOADED_HOMEWORKSUBMITS_DEST'],
                           evaluation.filename, 
                           as_attachment=True)
    else:
        return 'No permission to view file'


@cdn_blueprint.route('/resource/video/<resource_id>', methods=["GET", "POST"])
@login_required
def resource_video(resource_id):
    resource = Resource.query.get(resource_id)
    return send_from_directory(current_app.config['UPLOAD_VIDEO_FOLDER'],
                        resource.filename, 
                           as_attachment=True)
    # as_attachment=True


@cdn_blueprint.route('/lightcourse/resource/video/<resource_id>', methods=["GET", "POST"])
@login_required
def light_resource_video(resource_id):
    resource = LightResource.query.get(resource_id)
    return send_from_directory(current_app.config['UPLOAD_VIDEO_FOLDER'],
                        resource.filename, 
                           as_attachment=True)


@cdn_blueprint.route('/lightcourse/resource/photo/<resource_id>', methods=["GET", "POST"])
@login_required
def light_resource_photo(resource_id):
    resource = LightResource.query.get(resource_id)
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],
                        resource.filename, 
                           as_attachment=True)


@cdn_blueprint.route('/lightcourse/resource/doc/<resource_id>', methods=["GET", "POST"])
@login_required
def light_resource_doc(resource_id):
    resource = LightResource.query.get(resource_id)
    return send_from_directory(current_app.config['UPLOADED_ALLDOCS_DEST'],
                        resource.filename, 
                           as_attachment=True)


@cdn_blueprint.route('/light_homework/<hwork_id>', methods=["GET", "POST"])
@login_required
def light_homework(hwork_id):
    hwork = LightHomework.query.get(hwork_id)
    return send_from_directory(current_app.config['UPLOADED_DOCS_DEST'],
                           hwork.filename, 
                           as_attachment=True)


@cdn_blueprint.route('/light_homework/submitted/<submission_id>', methods=["GET", "POST"])
@login_required
def light_homework_submitted(submission_id):
    submission = LightHomeworkSubmission.query.get(submission_id)
    teacher_id = submission.chapter.course.teacher_id
    if (current_user.id == submission.course_taker_id or 
        current_user.role == 'admin' or
        current_user.id == teacher_id
        ):
        return send_from_directory(current_app.config['UPLOADED_HOMEWORKSUBMITS_DEST'],
                           submission.filename, 
                           as_attachment=True)
    else:
        return 'No permission to view file'


@cdn_blueprint.route('/light_homework/evaluated/<evaluation_id>', methods=["GET", "POST"])
@login_required
def light_homework_evaluated(evaluation_id):
    evaluation = LightHomeworkEvaluation.query.get(evaluation_id)
    teacher_id = evaluation.chapter.course.teacher_id
    if (current_user.id == evaluation.course_taker_id or 
        current_user.role == 'admin' or
        current_user.id == teacher_id
        ):
        return send_from_directory(current_app.config['UPLOADED_HOMEWORKSUBMITS_DEST'],
                           evaluation.filename, 
                           as_attachment=True)
    else:
        return 'No permission to view file'


@cdn_blueprint.route('/light_certificate/<course_id>', methods=["GET", "POST"])
@login_required
def light_certificate(course_id):
    # app.config['UPLOAD_FOLDER']
    certif = LightCertificate.query.filter(
        (LightCertificate.course_taker_id == current_user.id) &
        (LightCertificate.course_id == course_id)
        ).first() # course completed
    if certif:
        # '''
        return send_from_directory(current_app.config['UPLOAD_CERTIFICATES_FOLDER'],
                           certif.filename)
        # '''
        '''
        return '{}<br>{}'.format(current_app.config['UPLOAD_CERTIFICATES_FOLDER'],
            certif.filename)
            '''
    else:
        return "You can't view this certificate"

@cdn_blueprint.route('/school/logo', methods=["GET", "POST"])
def school_logo():
    logo = Setting.query.filter(
            Setting.name == 'logo'
        ).first()
    if logo.value is None:
        return send_from_directory(current_app.config['SCHOOL_DEFAULTS'],
                            'logo.png', as_attachment=True)
    else:
        return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],
                            logo.value, as_attachment=True)