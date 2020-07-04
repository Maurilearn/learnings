import os

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

from modules.auth.access import roles_required

from shopyoapi.enhance import base_context
from shopyoapi.init import photos

from .models import Setting

from .forms import AddLogoForm

school_blueprint = Blueprint(
    "school",
    __name__,
    url_prefix='/school',
    template_folder="templates",
)

@school_blueprint.after_request
def school_after_request(response):
    if current_user and current_user.is_authenticated:
        if current_user.check_hash(current_app.config['DEFAULT_PASS_ALL']):
            flash(notify_info('Change default password please to get access!'))
            return redirect(url_for('auth.change_pass', user_id=current_user.id))
        return response


@school_blueprint.route("/")
@roles_required(['admin'])
@login_required
def index():
    context = base_context()
    context['add_logo_form'] = AddLogoForm()
    context['school_name'] = Setting.query.filter(
            Setting.name == 'school_name'
        ).first().value
    context['contact_mail'] = Setting.query.filter(
            Setting.name == 'contact_mail'
        ).first().value
    context['logo'] = Setting.query.filter(
            Setting.name == 'logo'
        ).first().value
    return render_template('school/index.html', **context)


@school_blueprint.route("/info/update/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def info_update_check():
    if request.method == 'POST':
        school_name_input = request.form['school_name']
        contact_mail_input = request.form['contact_mail']

        school_name = Setting.query.filter(
            Setting.name == 'school_name'
        ).first()
        school_name.value = school_name_input
        school_name.update()

        contact_mail = Setting.query.filter(
            Setting.name == 'contact_mail'
        ).first()
        contact_mail.value = contact_mail_input
        contact_mail.update()

        flash(notify_success('Info updated!'))
        return redirect(url_for('school.index'))


@school_blueprint.route("/logo/add/check", methods=['GET', 'POST'])
@roles_required(['admin'])
@login_required
def add_logo_check():
    form = AddLogoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = photos.save(request.files[form.file_input.data.name])
            logo = Setting.query.filter(
                Setting.name == 'logo'
            ).first()
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], logo.value))
            logo.value = filename
            logo.update()
            flash(notify_success('Logo uploaded'))
            return redirect(url_for('school.index'))
        else:
            flash_errors(form)
            return redirect(url_for('school.index'))
