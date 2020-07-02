import json
import os
import datetime

from werkzeug import secure_filename

from modules.auth.access import roles_required

from modules.auth.models import User
from modules.course.models import Grade
from .models import LightAnswer
from .models import LightQuiz
from .models import LightCourse
from .models import LightChapter
from .models import LightResource
from .models import LightHomework
from .models import LightHomeworkSubmission
from .models import LightHomeworkEvaluation
from .models import LightQuizHistory
from .models import LightCertificateRequest
from .models import LightCertificate

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
from userapi.certificate import create_certificate
from userapi.file import file_prefix

from shopyoapi.enhance import base_context
from shopyoapi.init import alldocs
from shopyoapi.init import docs
from shopyoapi.init import photos
from shopyoapi.init import homeworksubmits

from .forms import AddLightCourseForm
from .forms import AddLightChapterForm
from .forms import AddTextForm
from .forms import AddDocsForm
from .forms import AddHomeworkForm
from .forms import AddPhotosForm
from .forms import SubmitHomeworkForm
from .forms import AddHomeworkNoteForm



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
    context['NUM_QUIZ'] = current_app.config['LIGHTCOURSE_QUIZ_NUM']
    return render_template('lightcourse/add.html', **context)

@lightcourse_blueprint.route("/add/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def add_check():
    if request.method == 'POST':
        data = request.get_json()
        
        course_name = data['course_name']
        course = LightCourse(name=course_name)
        
        grade_id = data['grade_id']
        course.grade = Grade.query.get(grade_id)

        for quiz in data['quizes']:
            question = json.dumps(data['quizes'][quiz]['question'])
            current_quiz = LightQuiz(question=question)
            answers = data['quizes'][quiz]['answers']
            for answer in answers:
                ans = json.dumps(answer['string'])
                current_quiz.answers.append(
                    LightAnswer(string=ans, correct=answer['correct']))
            course.quizzes.append(current_quiz)

        for chapter in data['chapters']:
            chapter_name = chapter['name']
            chapter_text = chapter['text']

            chapter = LightChapter(name=chapter_name)
            chapter.resources.append(LightResource(text=chapter_text))
            course.chapters.append(chapter)

        course.teacher_id = current_user.id
        course.insert()
        flash(notify_success('course added!'))
        return jsonify({"submission": "ok"})

@lightcourse_blueprint.route("/<course_id>/view", methods=['GET', 'POST'])
@login_required
def view(course_id):
    context = base_context()
    course = LightCourse.query.get(course_id)
    form = AddLightChapterForm()
    context['course'] = course
    context['form'] = form
    context['User'] = User

    def quiz_completed():
        if LightQuizHistory.query.filter(
                (LightQuizHistory.person_id == current_user.id) &
                (LightQuizHistory.light_course_id == course.id)
                ).first():
            return True
        return False
    def request_exists():
        if LightCertificateRequest.query.filter(
                (LightCertificateRequest.course_taker_id == current_user.id) &
                (LightCertificateRequest.course_id == course.id)
                ).first():
            return True
        return False

    def certif_approved():
        if LightCertificate.query.filter(
                (LightCertificate.course_taker_id == current_user.id) &
                (LightCertificate.course_id == course.id)
                ).first():
            return True
        return False


    context['quiz_completed'] = quiz_completed
    context['request_exists'] = request_exists
    context['certif_approved'] = certif_approved
    return render_template('lightcourse/view.html', **context)


@lightcourse_blueprint.route("/<course_id>/edit/name/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def edit_course_name_check(course_id):
    if request.method == 'POST':
        course = LightCourse.query.get(course_id)
        if not (current_user.id == course.teacher_id or current_user.role == 'admin'):
            return "You don't have permission to edit"
        course_name = request.form['course_name']
        if course_name.strip():
            course.name = course_name
            course.update()
            flash(notify_success('Course name updated!'))
            return redirect(url_for('lightcourse.view', course_id=course_id))
        else:
            flash(notify_warning('Course name cannot be empty!'))
            return redirect(url_for('lightcourse.view', course_id=course_id))



@lightcourse_blueprint.route("/<course_id>/delete", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def delete(course_id):

    course  = LightCourse.query.get(course_id)
    course.delete()
    flash(notify_danger('course deleted!'))
    return redirect(url_for('course.index'))


@lightcourse_blueprint.route("/<course_id>/add/chapter", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def add_chapter_check(course_id):
    form = AddLightChapterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            course = LightCourse.query.get(course_id)
            course.chapters.append(LightChapter(name=form.name.data))
            course.update()
        else:
            flash_errors(form)

    return redirect(url_for('lightcourse.view', course_id=course_id))


@lightcourse_blueprint.route("/chapter/<chapter_id>/edit/name/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def chapter_name_edit_check(chapter_id):
    if request.method == 'POST':
        chapter = LightChapter.query.get(chapter_id)
        course = chapter.course
        if not (current_user.id == course.teacher_id or current_user.role == 'admin'):
            return "You don't have permission to edit"
        chapter_name = request.form['chapter_name']
        if chapter_name.strip():
            chapter.name = chapter_name
            chapter.update()
            flash(notify_success('Chapter name updated!'))
            return redirect(url_for('lightcourse.view', course_id=course.id))
        else:
            flash(notify_warning('Chapter name cannot be empty!'))
            return redirect(url_for('lightcourse.view', course_id=course.id))


@lightcourse_blueprint.route("/view/chapter/<chapter_id>", methods=['GET', 'POST'])
@login_required
def view_chapter(chapter_id):
    context = base_context()
    chapter = LightChapter.query.get(chapter_id)
    context['chapter'] = chapter
    context['render_md'] = render_md
    context['add_text_form'] = AddTextForm()
    context['add_docs_form'] = AddDocsForm()
    context['add_photos_form'] = AddPhotosForm()
    context['add_homework_form'] = AddHomeworkForm()
    context['submit_homework_form'] = SubmitHomeworkForm()
    return render_template('lightcourse/view_chapter.html', **context)


@lightcourse_blueprint.route("/resource/<resource_id>/text/edit/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def resource_text_edit_check(resource_id):
    if request.method == 'POST':
        resource = LightResource.query.get(resource_id)
        chapter_id = resource.chapter.id
        resource.text = request.form['text_value']
        resource.update()
        return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))

@lightcourse_blueprint.route("/chapter/<chapter_id>/add/text/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def chapter_add_text_check(chapter_id):
    if request.method == 'POST':
        form = AddTextForm()
        chapter = LightChapter.query.get(chapter_id)
        chapter.resources.append(LightResource(text=form.text.data))
        chapter.update()
        return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))

@lightcourse_blueprint.route("/resource/<resource_id>/delete", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def resource_delete(resource_id):
    resource = LightResource.query.get(resource_id)
    chapter_id = resource.chapter.id
    if resource.type == 'doc':
        os.remove(os.path.join(current_app.config['UPLOADED_ALLDOCS_DEST'], resource.filename))
    elif resource.type == 'photo':
        os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], resource.filename))
    elif resource.type == 'video':
        os.remove(os.path.join(current_app.config['UPLOAD_VIDEO_FOLDER'], resource.filename))
    resource.delete()
    return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))


def video_allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp4', 'avi'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@lightcourse_blueprint.route("/chapter/<chapter_id>/add/video/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def resource_add_video_check(chapter_id):
    if request.method == 'POST':
        try:
            os.mkdir(current_app.config['UPLOAD_VIDEO_FOLDER'])
        except Exception as e:
            pass
        chapter = LightChapter.query.get(chapter_id)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(notify_warning('Video file empty!'))
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash(notify_warning('No selected file'))
            return redirect(request.url)
        if file and video_allowed_file(file.filename):
            filename = '{}_{}'.format(file_prefix(), secure_filename(file.filename))
            resource = LightResource(type='video', filename=filename)
            chapter.resources.append(resource)
            chapter.update()
            file.save(os.path.join(current_app.config['UPLOAD_VIDEO_FOLDER'], filename))
            flash(notify_success('Video uploaded!'))
            return redirect(url_for('lightcourse.view_chapter',
                                        chapter_id=chapter_id))



@lightcourse_blueprint.route("/chapter/<chapter_id>/add/docs/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def resource_add_alldocs_check(chapter_id):
    form = AddDocsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = alldocs.save(request.files[form.file_input.data.name])
            # filename = '{}_{}'.format(file_prefix(), filename)
            resource = LightResource(type='doc', filename=filename)
            chapter = LightChapter.query.get(chapter_id)
            chapter.resources.append(resource)
            chapter.update()
            flash(notify_success('Document file uploaded'))
        else:
            flash_errors(form)
    return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))



@lightcourse_blueprint.route("/chapter/<chapter_id>/add/photos/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def resource_add_photos_check(chapter_id):
    form = AddPhotosForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = photos.save(request.files[form.file_input.data.name])
            resource = LightResource(type='photo', filename=filename)
            chapter = LightChapter.query.get(chapter_id)
            chapter.resources.append(resource)
            chapter.update()
            flash(notify_success('Photo file uploaded'))
        else:
            flash_errors(form)
    return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))


@lightcourse_blueprint.route("/chapter/<chapter_id>/add/homework/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def add_homework_check(chapter_id):
    form = AddHomeworkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = docs.save(request.files[form.file_input.data.name])
            homework = LightHomework(filename=filename)
            chapter = LightChapter.query.get(chapter_id)
            chapter.homeworks.append(homework)
            chapter.update()
            flash(notify_success('Homework file uploaded'))
        else:
            flash_errors(form)
    return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))



@lightcourse_blueprint.route("/chapter/<chapter_id>/submit/homework/check", methods=['GET', 'POST'])
@login_required
def submit_homework_check(chapter_id):
    form = SubmitHomeworkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = homeworksubmits.save(request.files[form.file_input.data.name])
            homework_submit = LightHomeworkSubmission(filename=filename, course_taker_id=current_user.id)
            chapter = LightChapter.query.get(chapter_id)
            chapter.homework_submissions.append(homework_submit)
            chapter.update()
            flash(notify_success('Homework file submitted for evaluation'))
        else:
            flash_errors(form)
    return redirect(url_for('lightcourse.view_chapter', chapter_id=chapter_id))

@lightcourse_blueprint.route("/homework/submission/<submission_id>/evaluate", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def evaluate_homework_submission(submission_id):
    context = base_context()
    context['submission'] = LightHomeworkSubmission.query.get(submission_id)
    context['User'] = User
    form = AddHomeworkNoteForm()
    context['form'] = form
    return render_template('lightcourse/evaluate_homework.html', **context)


@lightcourse_blueprint.route("/homework/submission/<submission_id>/evaluate/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def evaluate_homework_submission_check(submission_id):
    if request.method == 'POST':
        form = AddHomeworkNoteForm()
        if form.validate_on_submit():
            submission = LightHomeworkSubmission.query.get(submission_id)
            course_taker_id = submission.course_taker_id
            chapter_id = submission.chapter_id
            notes = form.notes.data
            hwork_eval = LightHomeworkEvaluation(
                course_taker_id=course_taker_id,
                chapter_id=chapter_id,
                notes=notes,
                filename=submission.filename
                )
            submission.delete()
            hwork_eval.insert()
        else:
            flash_errors(form)
        return redirect(url_for('course.view_homework_submissions'))

@lightcourse_blueprint.route("/<course_id>/quiz", methods=['GET', 'POST'])
@login_required
def take_quiz(course_id):
    context = base_context()
    course = LightCourse.query.get(course_id)
    context['course'] = course
    # https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    return render_template('lightcourse/take_quiz.html', **context)


@lightcourse_blueprint.route("/<course_id>/quiz/check", methods=['GET', 'POST'])
@login_required
def check_quiz(course_id):
    if request.method == 'POST':
        correct_answers = 0
        # flash(notify_info(request.form))
        course = LightCourse.query.get(course_id)
        submitted_quiz = [name for name in request.form if name.startswith('quiz_')]
        # flash(notify_info(submitted_quiz))
        db_json  = {}
        if len(submitted_quiz) == 0:
            flash(notify_warning("Can't be empty"))
        else:
            quiz_seen = {}
            for quiz_name in submitted_quiz:
                info = quiz_name.split('_')
                q_id = info[1]
                a_id = info[3]
                if q_id not in quiz_seen:
                    quiz_seen[int(q_id)] = []
                quiz_seen[int(q_id)].append(int(a_id))
            # flash(notify_info(quiz_seen))
            if len(quiz_seen) != current_app.config['LIGHTCOURSE_QUIZ_NUM']:
                flash(notify_warning('All questions must be answered!'))
            
            else:
                for quiz in course.quizzes:
                    db_json[quiz.id] = []
                    for answer in quiz.answers:
                        if answer.correct == True:
                            db_json[quiz.id].append((answer.id))
                # flash(notify_info(db_json))

                for q in db_json:
                    if quiz_seen[q] == db_json[q]:
                        correct_answers += 1
                
                if (correct_answers/current_app.config['LIGHTCOURSE_QUIZ_NUM'])*100 >= 50:
                    quiz_history = LightQuizHistory(person_id=current_user.id, light_course_id=course.id)
                    quiz_history.insert()
                    flash(notify_success('Great! correct answers: {}/{}'.format(correct_answers,
                        current_app.config['LIGHTCOURSE_QUIZ_NUM'])))
                else:
                    flash(notify_warning('Oh oh! correct answers: {}/{}'.format(correct_answers,
                        current_app.config['LIGHTCOURSE_QUIZ_NUM'])))
        return redirect(url_for('lightcourse.take_quiz', course_id=course.id))


@lightcourse_blueprint.route("/<course_id>/certificate/request", methods=['GET', 'POST'])
@login_required
def request_certificate(course_id):
    req = LightCertificateRequest(
        course_id=course_id,
        course_taker_id=current_user.id
        )
    req.insert()
    return redirect(url_for('lightcourse.view', course_id=course_id))


@lightcourse_blueprint.route("/certificate/<certif_req_id>/approve", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def approve_certif_req(certif_req_id):
    certif_request = LightCertificateRequest.query.get(certif_req_id)
    course = LightCourse.query.get(certif_request.course_id)
    if not course:
        flash(notify_warning('Course no longer exist'))
        certif_request.delete()
        return redirect(url_for('course.view_certificate_request'))
    if not (current_user.id == course.teacher_id or current_user.role == 'admin'):
        return "You don't have permission to approve"
    course_taker_id = certif_request.course_taker_id
    course_id = certif_request.course_id
    certif_request.delete()
    certif = LightCertificate(
        course_taker_id=course_taker_id,
        course_id=course_id
        )
    

    person = User.query.get(course_taker_id)
    course = LightCourse.query.get(course_id)
    person_name = person.name.replace(' ', '_').replace('-', '_')
    course_name = course.name.replace(' ', '_')
    #flash(notify_info('{}'.format(os.getcwd())))
    
    try:
        dirname = current_app.config['UPLOAD_CERTIFICATES_FOLDER']
        try:
            os.mkdir(dirname)
        except:
            pass
        filename = "{}_{}.pdf".format(person_name, course_name)
        fname = os.path.join(dirname, filename)
        # flash(notify_info(fname))
        #with open(fname, 'w+') as f:
        #    f.write('')
        create_certificate(fname, person.name, course.name)
        certif.filename = filename
        certif.insert()
    except Exception as e:
        flash(notify_danger('{}'.format(e)))
    return redirect(url_for('course.view_certificate_request'))


@lightcourse_blueprint.route("/certificate/<certif_req_id>/decline", methods=['GET', 'POST'])
@login_required
def decline_certif_req(certif_req_id):
    certif_request = LightCertificateRequest.query.get(certif_req_id)
    course_taker_id = certif_request.course_taker_id
    course_id = certif_request.course_id
    course = lightCourse.query.get(course_id)
    if not course:
        flash(notify_warning('Course no longer exist'))
        certif_request.delete()
        return redirect(url_for('course.view_certificate_request'))
    if not (current_user.id == course.teacher_id or current_user.role == 'admin'):
        return "You don't have permission to approve"
    certif_request.delete()
    return redirect(url_for('course.view_certificate_request'))


@lightcourse_blueprint.route("/<course_id>/subscribe", methods=['GET', 'POST'])
@login_required
def toggle_subscribe(course_id):
    course = LightCourse.query.get(course_id)
    if course not in current_user.light_courses:
        current_user.light_courses.append(course)
        current_user.update()
        flash(notify_success('Subscribed to {}!'.format(course.name)))
    elif course in current_user.light_courses:
        current_user.light_courses.remove(course)
        current_user.update()
        flash(notify_warning('Unsubscribed from {}!'.format(course.name)))
    return redirect(url_for('course.list'))


@lightcourse_blueprint.route("/<course_id>/quiz/edit", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def edit_quiz(course_id):
    '''
    var init_json_submit = {
            "section_name": "",
            "quizes":{
                
            }
        }
        /*answer {"string":"", "correct":""}*/
        var empty_quiz = {
            "question":"",
            "answers":[
                
            ]
        }
    '''
    context = base_context()
    course = LightCourse.query.get(course_id)
    context['course'] = course
    context['NUM_QUIZ'] = current_app.config['LIGHTCOURSE_QUIZ_NUM']
    return render_template('lightcourse/edit_quiz.html', **context)


@lightcourse_blueprint.route("/<course_id>/quiz/edit/check", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
@login_required
def edit_quiz_check(course_id):
    try:
        if request.method == 'POST':
            # flash(notify_info('entered post'))
            data = request.get_json()
            course = LightCourse.query.get(course_id)
            course.quizzes[:] = []
            # flash(notify_info('cleared quizes'))
            for quiz in data['quizes']:
                question = data['quizes'][quiz]['question']
                question = json.dumps(question)
                current_quiz = LightQuiz(question=question)
                answers = data['quizes'][quiz]['answers']
                for answer in answers:
                    ans = answer['string']
                    ans = json.dumps(ans)
                    current_quiz.answers.append(
                        LightAnswer(string=ans, correct=answer['correct']))
                course.quizzes.append(current_quiz)
            
            course.update()
            flash(notify_info('updated'))
            return jsonify({
                "submission": "ok",
                "go_to":url_for('lightcourse.view', course_id=course_id)})
    except Exception as e:
        # flash(notify_warning(e))
        # flash(notify_info(data))
        return jsonify({
            "submission": "bad"})


@lightcourse_blueprint.route("/<course_id>/unsubscribe", methods=['GET', 'POST'])
@login_required
def unsubscribe(course_id):
    course = LightCourse.query.get(course_id)
    flash(notify_warning('Unsubscribed from {}!'.format(course.name)))
    current_user.light_courses.remove(course)
    current_user.update()
    
    return redirect(url_for('course.mycourses'))