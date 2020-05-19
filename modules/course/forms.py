from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms import TextAreaField


class AddCourseForm(FlaskForm):
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


class AddSectionForm(FlaskForm):
    name = StringField('Section Name', [
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

# chapter
class AddSubSectionForm(FlaskForm):
    name = StringField('Chapter Name', [
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

# "rows": 70,
class AddTextForm(FlaskForm):
    text = TextAreaField('Text', [
        DataRequired()
        ],
        render_kw={
                "rows": 20,
                "class": "form-control"
            }
        )
    submit = SubmitField('Submit',
        render_kw={
            'class':'btn btn-info'
            }
        )