import datetime
import os

from modules.auth.models import User
from .models import Course
from .models import Section
from .models import SubSection
from .models import Resource
from .models import QuizHistory
from .models import CertificateRequest
from .models import Certificate
from .models import Homework
from .models import HomeworkSubmission
from .models import HomeworkEvaluation

from .forms import AddCourseForm
from .forms import AddSectionForm
from .forms import AddSubSectionForm
from .forms import AddTextForm
from .forms import AddHomeworkForm
from .forms import SubmitHomeworkForm
from .forms import AddHomeworkNoteForm

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.init import fake
from shopyoapi.init import docs
from shopyoapi.init import homeworksubmits
from shopyoapi.enhance import base_context

from userapi.renders import render_md
from userapi.html import notify_danger
from userapi.html import notify_success
from userapi.html import notify_info
from userapi.html import notify_warning
from userapi.forms import flash_errors
from modules.quiz.models import Quiz
from modules.quiz.models import Answer

from reportlab.pdfgen import canvas



course_blueprint = Blueprint(
    "course",
    __name__,
    url_prefix='/course',
    template_folder="templates",
)


@course_blueprint.route("/")
@login_required
def index():
    context = base_context()
    # context['courses'] = [fake.paragraph(nb_sentences=1) for i in range(5)]
    context['User'] = User
    context['courses'] = Course.query.all()
    return render_template('course/index.html', **context)

@course_blueprint.route("/add")
@login_required
def add():
    context = base_context()
    context['form'] = AddCourseForm()
    return render_template('course/add_course.html', **context)


@course_blueprint.route("/add/check", methods=['GET', 'POST'])
@login_required
def add_check():
    context = base_context()
    if request.method == 'POST':
        form = AddCourseForm()
        course = Course(
            name=form.name.data,
            teacher_id=current_user.id
            )
        course.insert()
    return redirect(url_for('course.add'))

@course_blueprint.route("/view/<course_id>", methods=['GET', 'POST'])
@login_required
def view(course_id):
    context = base_context()
    course = Course.query.get(course_id)
    context['course'] = course
    context['author'] = User.query.get(course.teacher_id)
    def section_quiz_completed(current_user, section):
        if QuizHistory.query.filter(
                (QuizHistory.person_id == current_user.id) &
                (QuizHistory.section_id == section.id)
                ).first():
            return True
        return False

    def course_completed(course_id):
        '''
        quizhistory filter 
            qhistory.person.id == current.id and 
            qhistory.section.course.id == course id
        
        if QuizHistory.query.filter(
                (QuizHistory.person_id == current_user.id) &
                (QuizHistory.section.course.id == course_id)
                ).count() == len(course.sections):
        '''
        course = Course.query.get(course_id)
        person_quiz = QuizHistory.query.filter(
                (QuizHistory.person_id == current_user.id)
                ).all()
        completed_sections = []
        for completed in person_quiz:
            section = Section.query.get(completed.section_id)
            if section.course.id == course.id:
                completed_sections.append(completed)
        if len(completed_sections) == len(course.sections):
            return True
        return False

    def certificate_requested(course_id):
        if CertificateRequest.query.filter(
                (CertificateRequest.course_taker_id == current_user.id) &
                (CertificateRequest.course_id == course_id)
                ).first():
            return True
        return False

    def certificate_approved(course_id):
        if Certificate.query.filter(
                (Certificate.course_taker_id == current_user.id) &
                (Certificate.course_id == course_id)
                ).first():
            return True
        return False

    context['section_quiz_completed'] = section_quiz_completed
    context['course_completed'] = course_completed
    context['certificate_requested'] = certificate_requested
    context['certificate_approved'] = certificate_approved

    return render_template('course/view_course.html', **context)

@course_blueprint.route("/<course_id>/add/section")
@login_required
def add_section(course_id):
    context = base_context()
    course = Course.query.get(course_id)
    context['course'] = course
    context['author'] = User.query.get(course.teacher_id)
    # context['form'] = AddSectionForm()
    return render_template('course/add_section.html', **context)


@course_blueprint.route("/<course_id>/add/section/check", methods=['GET', 'POST'])
@login_required
def add_section_check(course_id):
    if request.method == 'POST':
        data = request.get_json()
        section_name = data['section_name']
        section = Section(name=section_name)
        for quiz in data['quizes']:
            question = data['quizes'][quiz]['question']
            current_quiz = Quiz(question=question)
            answers = data['quizes'][quiz]['answers']
            for answer in answers:
                current_quiz.answers.append(
                    Answer(string=answer['string'], correct=answer['correct']))
            section.quizzes.append(current_quiz)
        course = Course.query.get(course_id)
        course.sections.append(section)
        course.update()
        return jsonify({"submission": "ok"})

@course_blueprint.route("/section/<section_id>/delete")
@login_required
def delete_section(section_id):
    section = Section.query.get(section_id)
    course_id = section.course.id
    section.delete()
    flash(notify_danger('Deleted section {}!'.format(section.name)))
    return redirect(url_for('course.view', course_id=course_id))

@course_blueprint.route("/section/<section_id>/add/subsection")
@login_required
def add_subsection(section_id):
    context = base_context()
    section = Section.query.get(section_id)
    context['section'] = section
    context['form'] = AddSubSectionForm()
    return render_template('course/add_subsection.html', **context)


@course_blueprint.route("/section/<section_id>/add/subsection/check", methods=['GET', 'POST'])
@login_required
def add_subsection_check(section_id):
    if request.method == 'POST':
        form = AddSubSectionForm()
        section = Section.query.get(section_id)
        section.sub_sections.append(SubSection(name=form.name.data))
        section.update()
    return redirect(url_for('course.add_subsection', section_id=section_id))

@course_blueprint.route("/subsection/<subsection_id>", methods=['GET', 'POST'])
@login_required
def view_subsection(subsection_id):
    context = base_context()
    subsection = SubSection.query.get(subsection_id)
    context['subsection'] = subsection
    context['render_md'] = render_md
    context['course'] = subsection.section.course
    submit_hwork_form = SubmitHomeworkForm()
    context['submit_hwork_form'] = submit_hwork_form
    context['user_homeworks_submitted'] = HomeworkSubmission.query.filter(
        (HomeworkSubmission.course_taker_id == current_user.id) &
        (HomeworkSubmission.subsection_id == subsection_id)
        ).all()
    context['user_homeworks_evaluated'] = HomeworkEvaluation.query.filter(
        (HomeworkEvaluation.course_taker_id == current_user.id) &
        (HomeworkEvaluation.subsection_id == subsection_id)
        ).all()
    return render_template('course/view_subsection.html', **context)


@course_blueprint.route("/subsection/<subsection_id>/add/homework", methods=['GET', 'POST'])
@login_required
def subsection_add_homework(subsection_id):
    context = base_context()
    context['form'] = AddHomeworkForm()
    context['subsection'] = SubSection.query.get(subsection_id)
    return render_template('course/add_homework.html', **context)



@course_blueprint.route("/subsection/<subsection_id>/add/homework/check", methods=['GET', 'POST'])
@login_required
def subsection_add_homework_check(subsection_id):
    form = AddHomeworkForm()


    if request.method == 'POST':
        if form.validate_on_submit():
            subsection = SubSection.query.get(subsection_id)
            filename = docs.save(request.files[form.homework_doc.data.name])
            subsection.homeworks.append(Homework(filename=filename))
            subsection.update()
            # flash(notify_info(form.homework_doc.data.name))
            flash(notify_success('Homework file uploaded'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added.')
    return redirect(url_for('course.subsection_add_homework', subsection_id=subsection_id))


@course_blueprint.route("/subsection/<subsection_id>/submit/homework/check", methods=['GET', 'POST'])
@login_required
def subsection_submit_homework_check(subsection_id):
    form = SubmitHomeworkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            subsection = SubSection.query.get(subsection_id)
            filename = homeworksubmits.save(request.files[form.homework_submit.data.name])
            subsection.homework_submissions.append(
                HomeworkSubmission(
                    filename=filename,
                    course_taker_id=current_user.id)
                )
            subsection.update()
            # flash(notify_info(form.homework_doc.data.name))
            flash(notify_success('Homework file submitted!'))
        else:
            flash_errors(form)
    return redirect(url_for('course.view_subsection', subsection_id=subsection_id))



@course_blueprint.route("/subsection/<subsection_id>/add/text")
@login_required
def subsection_add_text(subsection_id):
    context = base_context()
    form = AddTextForm()
    context['form'] = form
    context['subsection'] = SubSection.query.get(subsection_id)
    return render_template('course/add_text.html', **context)


@course_blueprint.route("/subsection/<subsection_id>/add/text/check", methods=['GET', 'POST'])
@login_required
def subsection_add_text_check(subsection_id):
    if request.method == 'POST':
        form = AddTextForm()
        subsection = SubSection.query.get(subsection_id)
        subsection.resources.append(Resource(text=form.text.data))
        subsection.insert()
        return redirect(url_for('course.subsection_add_text', subsection_id=subsection_id))

@course_blueprint.route("/resource/<resource_id>/delete", methods=['GET', 'POST'])
@login_required
def resource_delete(resource_id):
    resource = Resource.query.get(resource_id)
    subsection_id = resource.sub_section.id
    resource.delete()
    return redirect(url_for('course.view_subsection', subsection_id=subsection_id))

@course_blueprint.route("/section/<section_id>/quiz", methods=['GET', 'POST'])
@login_required
def take_quiz(section_id):
    context = base_context()

    section = Section.query.get(section_id)
    course_id = section.course.id
    context['section'] = section
    return render_template('course/take_quiz.html', **context)

@course_blueprint.route("/section/<section_id>/quiz/check", methods=['GET', 'POST'])
@login_required
def check_quiz(section_id):
    if request.method == 'POST':
        correct_answers = 0
        # flash(notify_info(request.form))
        section = Section.query.get(section_id)
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
            if len(quiz_seen) != 10:
                flash(notify_warning('All questions must be answered!'))
            
            else:
                for quiz in section.quizzes:
                    db_json[quiz.id] = []
                    for answer in quiz.answers:
                        if answer.correct == True:
                            db_json[quiz.id].append((answer.id))
                # flash(notify_info(db_json))

                for q in db_json:
                    if quiz_seen[q] == db_json[q]:
                        correct_answers += 1
                
                if (correct_answers/10)*100 >= 50:
                    quiz_history = QuizHistory(person_id=current_user.id, section_id=section.id)
                    quiz_history.insert()
                    flash(notify_success('Great! correct answers: {}/10'.format(correct_answers)))
                else:
                    flash(notify_warning('Oh oh! correct answers: {}/10'.format(correct_answers)))
        return redirect(url_for('course.take_quiz', section_id=section_id))


# for subs
@course_blueprint.route("/list", methods=['GET', 'POST'])
@login_required
def list():
    context = base_context()
    context['courses'] = Course.query.all()
    context['User'] = User
    context['current_user'] = current_user
    return render_template('course/list.html', **context)


@course_blueprint.route("/<course_id>/subscribe", methods=['GET', 'POST'])
@login_required
def toggle_subscribe(course_id):
    course = Course.query.get(course_id)
    if course not in current_user.courses:
        current_user.courses.append(course)
        current_user.update()
        flash(notify_success('Subscribed to {}!'.format(course.name)))
    elif course in current_user.courses:
        current_user.courses.remove(course)
        current_user.update()
        flash(notify_warning('Unsubscribed from {}!'.format(course.name)))
    return redirect(url_for('course.list'))


@course_blueprint.route("/mycourses", methods=['GET', 'POST'])
@login_required
def mycourses():
    context = base_context()
    mycourses = current_user.courses
    context['mycourses'] = mycourses
    context['User'] = User

    return render_template('course/mycourses.html', **context)


@course_blueprint.route("/<course_id>/unsubscribe", methods=['GET', 'POST'])
@login_required
def unsubscribe(course_id):
    course = Course.query.get(course_id)
    current_user.courses.remove(course)
    current_user.update()
    flash(notify_warning('Unsubscribed from {}!'.format(course.name)))
    return redirect(url_for('course.mycourses'))

#
# Certificates
#


@course_blueprint.route("/<course_id>/certificate/request", methods=['GET', 'POST'])
@login_required
def certificate_request(course_id):
    if CertificateRequest.query.filter(
                (CertificateRequest.course_taker_id == current_user.id) &
                (CertificateRequest.course_id == course_id)
                ).first():
        flash(notify_warning('Certificate being processed!'))
    else:
        cert_req = CertificateRequest(
            course_taker_id=current_user.id,
            course_id=course_id
            )
        cert_req.insert()
        flash(notify_success('Certificate requested!'))
    return redirect(url_for('course.view', course_id=course_id))

@course_blueprint.route("/view/certificate/request", methods=['GET', 'POST'])
@login_required
def view_certificate_request():
    if current_user.role in ['admin', 'teacher']:
        context = base_context()
        if current_user.role == 'admin':
            certif_requests = CertificateRequest.query.all()
            context['certif_requests'] = certif_requests
        else:
            c_requests = []
            for cert_request_item in CertificateRequest.query.all():
                course = Course.query.get(cert_request_item.course_id)
                if course.teacher_id == current_user.id:
                    c_requests.append(cert_request_item)
            context['certif_requests'] = c_requests
        context['User'] = User
        context['Course'] = Course
        return render_template('course/certificate_requests.html', **context)
    else:
        flash(notify_danger('Unauthorised attempt!'))
        return redirect(url_for('course.index'))


@course_blueprint.route("/certificate/<certif_req_id>/approve", methods=['GET', 'POST'])
@login_required
def approve_certif_req(certif_req_id):
    certif_request = CertificateRequest.query.get(certif_req_id)
    course = Course.query.get(certif_request.course_id)
    if not (current_user.id == course.teacher_id or current_user.role == 'admin'):
        return "You don't have permission to approve"
    course_taker_id = certif_request.course_taker_id
    course_id = certif_request.course_id
    certif_request.delete()
    certif = Certificate(
        course_taker_id=course_taker_id,
        course_id=course_id
        )
    

    person = User.query.get(course_taker_id)
    course = Course.query.get(course_id)
    person_name = person.name.replace(' ', '_').replace('-', '_')
    course_name = course.name.replace(' ', '_')
    #flash(notify_info('{}'.format(os.getcwd())))
    
    try:
        dirname = "static/certificates/"
        filename = "{}_{}.pdf".format(person_name, course_name)
        fname = dirname+filename
        with open(fname, 'w+') as f:
            f.write('')
        c = canvas.Canvas(fname)
        c.setTitle("Certificate")
        init_y = 250
        c.drawString(100, init_y,"Certificate Awarded To")
        init_y -= 20
        c.drawString(100, init_y, person.name)
        init_y -= 20
        c.drawString(100, init_y,"For")
        init_y -= 20
        c.drawString(100, init_y, course.name)
        init_y -= 20
        c.drawString(100, init_y, "On")
        init_y -= 20
        datetime_now = datetime.datetime.now()
        datenow = '{} - {} - {}'.format(
            datetime_now.year, 
            datetime_now.month, 
            datetime_now.day)
        c.drawString(100, init_y, datenow)
        c.save()
        certif.filename = filename
        certif.insert()
    except Exception as e:
        flash(notify_danger('{}'.format(e)))
    return redirect(url_for('course.view_certificate_request'))


@course_blueprint.route("/certificate/<certif_req_id>/decline", methods=['GET', 'POST'])
@login_required
def decline_certif_req(certif_req_id):
    certif_request = CertificateRequest.query.get(certif_req_id)
    course_taker_id = certif_request.course_taker_id
    course_id = certif_request.course_id
    certif_request.delete()
    return redirect(url_for('course.view_certificate_request'))

#
# Homework
#

@course_blueprint.route("/homework/submissions", methods=['GET', 'POST'])
@login_required
def view_homework_submissions():
    context = base_context()
    if current_user.role == 'admin':
        submissions = HomeworkSubmission.query.all()
    else:
        submissions = []
        for submission in HomeworkSubmission.query.all():
            subsection = SubSection.query.get(submission.subsection_id)
            teacher_id = submission.sub_section.section.course.teacher_id
            if current_user.id == teacher_id:
                submissions.append(submission)
    context['submissions'] = submissions
    context['User'] = User
    return render_template('course/view_submissions.html', **context)


@course_blueprint.route("/homework/submission/<submission_id>/evaluate", methods=['GET', 'POST'])
@login_required
def evaluate_homework_submission(submission_id):
    context = base_context()
    context['submission'] = HomeworkSubmission.query.get(submission_id)
    context['User'] = User
    form = AddHomeworkNoteForm()
    context['form'] = form
    return render_template('course/evaluate_homework.html', **context)


@course_blueprint.route("/homework/submission/<submission_id>/evaluate/check", methods=['GET', 'POST'])
@login_required
def evaluate_homework_submission_check(submission_id):
    if request.method == 'POST':
        form = AddHomeworkNoteForm()
        if form.validate_on_submit():
            submission = HomeworkSubmission.query.get(submission_id)
            course_taker_id = submission.course_taker_id
            subsection_id = submission.subsection_id
            notes = form.notes.data
            hwork_eval = HomeworkEvaluation(
                course_taker_id=course_taker_id,
                subsection_id=subsection_id,
                notes=notes,
                filename=submission.filename
                )

            submission.delete()
            hwork_eval.insert()
        else:
            flash_errors(form)
        return redirect(url_for('course.view_homework_submissions'))