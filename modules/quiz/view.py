

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash

from flask_login import login_required
from flask_login import current_user

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.init import fake
from shopyoapi.init import photos

from shopyoapi.enhance import base_context

from modules.course.models import SubSection
from .forms import AddTrackForm
from .models import Quiz

from config import Config

from os import path
from werkzeug import secure_filename

quiz_blueprint = Blueprint(
    "quiz",
    __name__,
    url_prefix='/quiz',
    template_folder="templates",
)


@quiz_blueprint.route("/")
@login_required
def index():
    context = base_context()
    context['tracks'] = QuizzTrack.query.all()
    return render_template('quiz/index.html', **context)


# @quiz_blueprint.route("/add/<subsection_id>")
# @login_required
# def quiz_add(subsection_id):
#     context = base_context()
#     context['subsection'] = SubSection
#     return render_template('quiz/add.html')


'''

@quizz_blueprint.route("/add/track/<track_id>")
@login_required
def quizz_add(track_id):
    context = base_context()
    context['track'] = QuizzTrack.query.get(track_id)

    return render_template('quizz/add_quizz.html', **context)

@quizz_blueprint.route("/add/track/<track_id>/check", methods=['GET', 'POST'])
@login_required
def quizz_add_check(track_id):
    if request.method == 'POST':
        track = QuizzTrack.query.get(track_id)
        answers = []
        quiz = Quizz(question=request.form['question'])
        for key in request.form:
            if key.startswith('answer'):
                ans_num = key.split('_')[1]
                correct = True
                try:
                    request.form['correct_'+ans_num]
                except KeyError:
                    correct = False
                answers.append(Answer(string=request.form[key], correct=correct))
        quiz.answers = answers
        track.quizzes.append(quiz)
        track.update()
        return redirect(url_for('quizz.quizz_add', track_id=track_id))

@quizz_blueprint.route("/delete/<quizz_id>", methods=['GET', 'POST'])
@login_required
def delete(quizz_id):
    quizz = Quizz.query.get(quizz_id)
    if quizz.quizz_track.creator.id == current_user.id or quizz.quizz_track.creator == 'admin':
        quizz.delete()
        return redirect(url_for('quizz.track_view', track_id=quizz.quizz_track.id))
    else:
        return 'Unauthorised deletion attempt'

@quizz_blueprint.route("/<quizz_id>/view", methods=['GET', 'POST'])
@login_required
def view(quizz_id):
    context = base_context()
    context['quizz'] = Quizz.query.get(quizz_id)

    return render_template('quizz/view_quizz.html', **context)

@quizz_blueprint.route("/<quizz_id>/update", methods=['GET', 'POST'])
@login_required
def quizz_update(quizz_id):
    if request.method == 'POST':
        quizz = Quizz.query.get(quizz_id)
        quizz.question = request.form['question']
        quizz.answers[:] = []
        answers = []
        for key in request.form:
            if key.startswith('answer'):
                ans_num = key.split('_')[1]
                correct = True
                try:
                    request.form['correct_'+ans_num]
                except KeyError:
                    correct = False
                answers.append(Answer(string=request.form[key], correct=correct))
        quizz.answers = answers
        quizz.update()
        return redirect(url_for('quizz.view', quizz_id=quizz_id))

@quizz_blueprint.route("/take/index", methods=['GET', 'POST'])
@login_required
def take_index():
    context = base_context()
    context['tracks'] = QuizzTrack.query.all()
    return render_template('quizz/take_quizz_index.html', **context)

@quizz_blueprint.route("/take/track/<track_id>", methods=['GET', 'POST'])
@login_required
def take_track(track_id):
    context = base_context()
    track = QuizzTrack.query.get(track_id)
    context['track'] = track
    return render_template('quizz/take_track.html', **context)

@quizz_blueprint.route("/debug", methods=['GET', 'POST'])
@login_required
def debug():
    if request.method == 'POST':
        context = base_context()
        context['text'] = request.form
        
        return render_template('quizz/debug.html', **context)
'''