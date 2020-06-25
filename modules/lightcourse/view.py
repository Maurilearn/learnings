import json
import os

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
@roles_required(['admin', 'teacher'])
@login_required
def view(course_id):
    context = base_context()
    course = LightCourse.query.get(course_id)
    form = AddLightChapterForm()
    context['course'] = course
    context['form'] = form
    context['User'] = User

    return render_template('lightcourse/view.html', **context)


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


@lightcourse_blueprint.route("/view/chapter/<chapter_id>", methods=['GET', 'POST'])
@roles_required(['admin', 'teacher'])
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
            filename = secure_filename(file.filename)
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
