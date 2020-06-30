from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms import TextAreaField
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired

from shopyoapi.init import photos

from .models import Setting


class AddLogoForm(FlaskForm):
    file_input = FileField('Add logo', validators=[
        FileAllowed(photos, 'Photo must be in png jpg or jpeg'),
        FileRequired('Photo was empty!')
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )


