from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today)
    content = TextAreaField('Content', validators=[DataRequired()])
    media_file = MultipleFileField('Upload Media',
                                   validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'mov', 'webm'])])
    submit = SubmitField('Post')
