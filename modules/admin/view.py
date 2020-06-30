from modules.auth.models import User

from .forms import AddAdminForm
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

admin_blueprint = Blueprint(
    "admin",
    __name__,
    url_prefix='/admin',
    template_folder="templates",
)

@admin_blueprint.after_request
def admin_after_request(response):
    if current_user.check_hash(current_app.config['DEFAULT_PASS_ALL']):
        flash(notify_info('Change default password please to get access!'))
        return redirect(url_for('auth.change_pass', user_id=current_user.id))
    return response

@admin_blueprint.route("/", methods=['GET'], defaults={"page": 1})
@admin_blueprint.route('/<int:page>', methods=['GET'])
@roles_required(['admin'])
@login_required
def index(page):
    context = base_context()
    page = page
    per_page = 5
    context = base_context()
    admin_query = User.query.filter(
        (User.role == 'admin')
    )
    context['admins'] = admin_query.paginate(page, per_page, error_out=False)

    context['number_records'] = len(admin_query.all())
    context['per_page'] = per_page
    form = AddAdminForm()
    context['form'] = form
    return render_template('admin/index.html', **context)

@admin_blueprint.route("/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_check():
    if request.method == 'POST':
        context = base_context()
        form = AddAdminForm()
        # if form.validate_on_submit():
        if not form.validate_on_submit():
            flash(notify_warning('Form not valid!'))
            return render_template(url_for('course.index'))
        user = User.query.filter(
            User.email == form.email.data
        ).first()
        if user:
            flash(notify_danger('Mail already exists!'))
            return redirect(url_for('admin.index'))
        admin = User(
                name=form.name.data,
                email=form.email.data,
                role='admin'
            )
        admin.set_hash(current_app.config['DEFAULT_PASS_ALL'])
        admin.insert()
        flash(notify_success('Added {}!'.format(admin.name)))
        return redirect(url_for('admin.index'))



@admin_blueprint.route("/edit/<admin_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def edit(admin_id):
    if request.method == 'POST':
        admin = User.query.get(admin_id)
        admin.name = request.form['admin_name']
        admin.email = request.form['admin_email']
        if request.form['admin_password'].strip() != '':
            admin.set_hash(request.form['admin_password'])
        admin.update()
        flash(notify_info('Saved {}!'.format(admin.name)))
        return redirect(url_for('admin.index'))


@admin_blueprint.route("/delete/<admin_id>", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def delete(admin_id):
    admin = User.query.get(admin_id)
    admin.delete()
    flash(notify_danger('Deleted {}!'.format(admin.name)))
    return redirect(url_for('admin.index'))
