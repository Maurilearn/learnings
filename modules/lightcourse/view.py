import json

from modules.auth.access import roles_required

from modules.course.models import Grade
from .models import LightAnswer
from .models import LightQuiz
from .models import LightCourse
from .models import LightChapter
from .models import LightResource

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



        '''
        section_name = data['section_name']
        section = Section(name=section_name)
        for quiz in data['quizes']:
            question = json.dumps(data['quizes'][quiz]['question'])
            current_quiz = Quiz(question=question)
            answers = data['quizes'][quiz]['answers']
            for answer in answers:
                ans = json.dumps(answer['string'])
                current_quiz.answers.append(
                    Answer(string=ans, correct=answer['correct']))
            section.quizzes.append(current_quiz)
        course = Course.query.get(course_id)
        course.sections.append(section)
        course.update()
        return jsonify({"submission": "ok"})
        '''