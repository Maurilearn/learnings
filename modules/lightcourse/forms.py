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
from shopyoapi.init import alldocs
from shopyoapi.init import photos

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


class AddLightChapterForm(FlaskForm):
    name = StringField('Name', [
        DataRequired()
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )
    submit = SubmitField('Submit',
        render_kw={
            'class':'btn btn-info'
            }
        )


class AddTextForm(FlaskForm):
    text = TextAreaField('Text', [
        DataRequired()
        ],
        render_kw={
                "rows": 10,
                "class": "form-control",
                "id":"add_text_text"
            }
        )
    submit = SubmitField('Submit',
        render_kw={
            'class':'btn btn-info'
            }
        )


class AddDocsForm(FlaskForm):
    file_input = FileField('Document', validators=[
        FileAllowed(alldocs, "Doc must be in ('.rtf', '.odf', '.ods', '.gnumeric', '.abw', '.doc', "
        "'.docx', '.xls', '.xlsx', '.ppt', '.pdf')"),
        FileRequired('Doc file was empty!')
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )


class AddPhotosForm(FlaskForm):
    file_input = FileField('Photo', validators=[
        FileAllowed(photos, 'Photo must be in png jpg or jpeg'),
        FileRequired('Photo was empty!')
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )

class AddHomeworkForm(FlaskForm):
    file_input = FileField('Homework', validators=[
        FileAllowed(docs, 'Homework must be in pdf odt or docx'),
        FileRequired('Homework was empty!')
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )