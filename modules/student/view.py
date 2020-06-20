from modules.auth.models import User
from modules.course.models import Grade

from .forms import AddStudentForm
from .forms import AddGradeForm
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

student_blueprint = Blueprint(
    "student",
    __name__,
    url_prefix='/student',
    template_folder="templates",
)

@student_blueprint.after_request
def student_after_request(response):
    if current_user:
        if current_user.is_authenticated:
            if current_user.check_hash(current_app.config['DEFAULT_PASS_ALL']):
                flash(notify_info('Change default password please to get access!'))
                return redirect(url_for('auth.change_pass', user_id=current_user.id))
    return response


@student_blueprint.route('/', methods=['GET'])
@roles_required(['admin'])
@login_required
def index():
    context = base_context()
    form = AddGradeForm()
    context['form'] = form
    context['grades'] = Grade.query.all()
    return render_template('student/index.html', **context)

@student_blueprint.route("/grade/edit/<grade_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def grade_edit(grade_id):
    if request.method == 'POST':
        grade = Grade.query.get(grade_id)
        grade.name = request.form['grade_name']
        grade.update()
        flash(notify_info('Saved {}!'.format(grade.name)))
        return redirect(url_for('student.index'))

@student_blueprint.route("/garde/delete/<grade_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def grade_delete(grade_id):
    grade = Grade.query.get(grade_id)
    grade.delete()
    flash(notify_danger('deleted grade {}!'.format(grade.name)))
    return redirect(url_for('student.index'))


@student_blueprint.route("/grade/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_grade_check():
    if request.method == 'POST':
        context = base_context()
        form = AddGradeForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            return redirect(url_for('student.index'))

        grade = Grade.query.filter(
            Grade.name == form.name.data
        ).first()
        if grade:
            flash(notify_danger('Grade already exists!'))
            return redirect(url_for('student.index'))
        grade = Grade(
                name=form.name.data
            )
        grade.insert()
        flash(notify_success('Added grade {}!'.format(form.name.data)))
        return redirect(url_for('student.index'))


@student_blueprint.route("/view/grade/<grade_id>/", methods=['GET'], defaults={"page": 1})
@student_blueprint.route('/view/grade/<grade_id>/<int:page>', methods=['GET'])
@roles_required(['admin'])
@login_required
def view(grade_id, page):
    page = page
    per_page = 5
    context = base_context()
    context['grade'] = Grade.query.get(grade_id)
    grade = Grade.query.get(grade_id)
    student_query = User.query.filter(
        (User.role == 'student') &
        (User.grade == grade)
    )
    context['students'] = student_query.paginate(page, per_page, error_out=False)
    form = AddStudentForm()
    context['form'] = form
    context['number_records'] = len(student_query.all())
    context['per_page'] = per_page
    # context['MESSAGES'] = [request.args.get('message', default='a')]
    return render_template('student/view_students.html', **context)


@student_blueprint.route("/grade/<grade_id>/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_check(grade_id):
    if request.method == 'POST':
        context = base_context()
        form = AddStudentForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            return redirect(url_for('student.index'))

        user = User.query.filter(
            User.email == form.email.data
        ).first()
        if user:
            flash(notify_danger('Mail already exists!'))
            return redirect(url_for('student.index'))
        student = User(
                name=form.name.data,
                email=form.email.data,
                role='student'
            )
        grade = Grade.query.get(grade_id)
        student.grade = grade
        student.set_hash(current_app.config['DEFAULT_PASS_ALL'])
        student.insert()
        flash(notify_success('Added {}!'.format(form.email.data)))
        return redirect(url_for('student.view', grade_id=grade_id))


@student_blueprint.route("/<student_id>/delete/", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def delete(student_id):
    student = User.query.get(student_id)
    student_grade = student.grade
    email= student.email
    student.delete()
    flash(notify_danger('deleted user {}!'.format(email)))
    return redirect(url_for('student.view', grade_id=student_grade.id))


@student_blueprint.route("/<student_id>/grade/<grade_id>/edit", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def edit(student_id, grade_id):
    if request.method == 'POST':
        student = User.query.get(student_id)
        student.name = request.form['student_name']
        student.email = request.form['student_email']
        if request.form['student_password'].strip() != '':
            student.set_hash(request.form['student_password'])
        student.update()
        flash(notify_info('Saved {}!'.format(student.name)))
        return redirect(url_for('student.view', grade_id=grade.id))

'''


@student_blueprint.route("/list/grade/<grade_id>/", methods=['GET'], defaults={"page": 1})
@student_blueprint.route('/list/grade/<grade_id>/<int:page>', methods=['GET'])
@roles_required(['admin'])
@login_required
def list_students(grade_id, page):
    page = page
    per_page = 5
    context = base_context()
    student_query = User.query.filter(
        (User.role == 'student')
    )
    context['students'] = student_query.paginate(page, per_page, error_out=False)
    form = AddStudentForm()
    context['form'] = form
    context['number_records'] = len(student_query.all())
    context['per_page'] = per_page
    # context['MESSAGES'] = [request.args.get('message', default='a')]
    return render_template('student/index.html', **context)

@student_blueprint.route("/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_check():
    if request.method == 'POST':
        context = base_context()
        form = AddStudentForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            return redirect(url_for('student.index'))

        user = User.query.filter(
            User.email == form.email.data
        ).first()
        if user:
            flash(notify_danger('Mail already exists!'))
            return redirect(url_for('student.index'))
        student = User(
                name=form.name.data,
                email=form.email.data,
                role='student'
            )
        student.set_hash(current_app.config['DEFAULT_PASS_ALL'])
        student.insert()
        flash(notify_success('Added {}!'.format(form.email.data)))
        return redirect(url_for('student.index'))


@student_blueprint.route("/edit/<student_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def edit(student_id):
    if request.method == 'POST':
        student = User.query.get(student_id)
        student.name = request.form['student_name']
        student.email = request.form['student_email']
        if request.form['student_password'].strip() != '':
            student.set_hash(request.form['student_password'])
        student.update()
        flash(notify_info('Saved {}!'.format(student.name)))
        return redirect(url_for('student.index'))


@student_blueprint.route("/delete/<student_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def delete(student_id):
    student = User.query.get(student_id)
    email= student.email
    student.delete()
    flash(notify_danger('deleted user {}!'.format(email)))
    return redirect(url_for('student.index'))
'''