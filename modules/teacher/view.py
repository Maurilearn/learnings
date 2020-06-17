from modules.auth.models import User

from modules.teacher.forms import AddTeacherForm
from modules.auth.access import roles_required

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import current_app

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.enhance import base_context

from userapi.html import notify_success
from userapi.html import notify_danger
from userapi.html import notify_info
from userapi.html import notify_warning

teacher_blueprint = Blueprint(
    "teacher",
    __name__,
    url_prefix='/teacher',
    template_folder="templates",
)

@teacher_blueprint.after_request
def teacher_after_request(response):
    if current_user.check_hash(current_app.config['DEFAULT_PASS_ALL']):
        flash(notify_info('Change default password please to get access!'))
        return redirect(url_for('auth.change_pass', user_id=current_user.id))
    return response

@teacher_blueprint.route("/", methods=['GET'], defaults={"page": 1})
@teacher_blueprint.route('/<int:page>', methods=['GET'])
@roles_required(['admin'])
@login_required
def index(page):
    context = base_context()
    page = page
    per_page = 5
    context = base_context()
    teacher_query = User.query.filter(
        (User.role == 'teacher')
    )
    context['teachers'] = teacher_query.paginate(page, per_page, error_out=False)

    context['number_records'] = len(teacher_query.all())
    context['per_page'] = per_page
    form = AddTeacherForm()
    context['form'] = form
    return render_template('teacher/index.html', **context)

@teacher_blueprint.route("/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_check():
    if request.method == 'POST':
        context = base_context()
        form = AddTeacherForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            flash(notify_warning('Form not valid!'))
            return render_template(url_for('course.index'))
        user = User.query.filter(
            User.email == form.email.data
        ).first()
        if user:
            flash(notify_danger('Mail already exists!'))
            return redirect(url_for('teacher.index'))
        teacher = User(
                name=form.name.data,
                email=form.email.data,
                role='teacher'
            )
        teacher.set_hash(current_app.config['DEFAULT_PASS_ALL'])
        teacher.insert()
        flash(notify_success('Added {}!'.format(teacher.name)))
        return redirect(url_for('teacher.index'))



@teacher_blueprint.route("/edit/<teacher_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
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
@roles_required(['admin'])
@login_required
def delete(teacher_id):
    teacher = User.query.get(teacher_id)
    teacher.delete()
    flash(notify_danger('Deleted {}!'.format(teacher.name)))
    return redirect(url_for('teacher.index'))
