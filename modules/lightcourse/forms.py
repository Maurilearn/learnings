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

from shopyoapi.init import docs


def grade_query():
    from modules.course.models import Grade
    return Grade.query.all()

class AddLightCourseForm(FlaskForm):
    name = StringField('Name', [
        DataRequired()
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )
    grade = QuerySelectField('Grade',
        query_factory=grade_query,
        allow_blank=False,
        blank_text="Click to select",
        render_kw={
            'class':'form-control'
            }
        )
    submit = SubmitField('Submit',
        render_kw={
            'class':'btn btn-info'
            }
        )