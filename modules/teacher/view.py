from modules.auth.models import User

from modules.teacher.forms import AddTeacherForm

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.enhance import base_context

from userapi.html import notify_success
from userapi.html import notify_danger
from userapi.html import notify_info


teacher_blueprint = Blueprint(
    "teacher",
    __name__,
    url_prefix='/teacher',
    template_folder="templates",
)


@teacher_blueprint.route("/")
def index():
    context = base_context()
    context['teachers'] = User.query.filter(
        (User.role == 'teacher')
    ).all()
    form = AddTeacherForm()
    context['form'] = form
    return render_template('teacher/index.html', **context)

@teacher_blueprint.route("/add/check", methods=['GET', 'POST'])
def add_check():
    if request.method == 'POST':
        context = base_context()
        form = AddTeacherForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            return render_template(url_for('course.index'))
        teacher = User(
                name=form.name.data,
                email=form.email.data,
                role='teacher'
            )
        teacher.set_hash(form.password.data)
        teacher.insert()
        flash(notify_success('Added {}!'.format(teacher.name)))
        return redirect(url_for('teacher.index'))


@teacher_blueprint.route("/edit/<teacher_id>", methods=['GET', 'POST'])
def edit(teacher_id):
    if request.method == 'POST':
        teacher = User.query.get(teacher_id)
        teacher.name = request.form['teacher_name']
        teacher.email = request.form['teacher_email']
        if request.form['teacher_password'].strip() != '':
            teacher.set_hash(request.form['teacher_password'])
        teacher.update()
        flash(notify_info('Saved {}!'.format(teacher.name)))
        return redirect(url_for('teacher.index'))


@teacher_blueprint.route("/delete/<teacher_id>", methods=['GET', 'POST'])
def delete(teacher_id):
    teacher = User.query.get(teacher_id)
    teacher.delete()
    flash(notify_danger('Deleted {}!'.format(teacher.name)))
    return redirect(url_for('teacher.index'))
