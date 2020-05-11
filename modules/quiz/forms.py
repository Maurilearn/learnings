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
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired

from shopyoapi.init import photos

class AddTrackForm(FlaskForm):
    name = StringField('Quizz Track Name', [
        DataRequired()
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )
    award_image = FileField('Award Image', validators=[
        FileAllowed(photos, 'Photo must be a png, jpg, or jpeg!'),
        FileRequired('File was empty!')
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

    # def __init__(self, *args, **kwargs):
    #     """Create instance."""
    #     super(AddTrackForm, self).__init__(*args, **kwargs)

    # def validate(self):
    #     """Validate the form."""

    #     initial_validation = super(AddTrackForm, self).validate()
    #     return not initial_validation