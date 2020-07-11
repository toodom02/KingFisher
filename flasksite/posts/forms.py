from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today)
    content = TextAreaField('Content', validators=[DataRequired()])
    media_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'mp4', 'mov', 'webm'])])
    submit = SubmitField('Post')
