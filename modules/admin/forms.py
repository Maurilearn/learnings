from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextField
from wtforms import SelectField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class AddAdminForm(FlaskForm):
    name = StringField('Name', [
        DataRequired()],
        render_kw={
            'class':'form-control',
            'autocomplete':'off'
            }
        )
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            }
        )
    submit = SubmitField('Submit',
        render_kw={
            'class':'btn btn-info',
            'value':'Submit'
            }
        )