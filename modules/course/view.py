from modules.auth.models import User
from modules.course.models import Course
from modules.course.models import Section
from modules.course.models import SubSection
from .models import Resource

from modules.course.forms import AddCourseForm
from modules.course.forms import AddSectionForm
from modules.course.forms import AddSubSectionForm
from modules.course.forms import AddTextForm

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
from shopyoapi.enhance import base_context

from userapi.renders import render_md
from userapi.html import notify_danger
from userapi.html import notify_success
from userapi.html import notify_info
from userapi.html import notify_warning

from modules.quiz.models import Quiz
from modules.quiz.models import Answer

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
    return render_template('course/view_subsection.html', **context)


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
        flash(notify_info(request.form))
        section = Section.query.get(section_id)
        submitted_quiz = [name for name in request.form if name.startswith('quiz_')]
        flash(notify_info(submitted_quiz))
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
            flash(notify_info(quiz_seen))
            if len(quiz_seen) != 10:
                flash(notify_warning('All questions must be answered!'))
            
            else:
                for quiz in section.quizzes:
                    db_json[quiz.id] = []
                    for answer in quiz.answers:
                        if answer.correct == True:
                            db_json[quiz.id].append((answer.id))
                flash(notify_info(db_json))

                for q in db_json:
                    if quiz_seen[q] == db_json[q]:
                        correct_answers += 1
                flash(notify_success('correct answers: {}'.format(correct_answers)))
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