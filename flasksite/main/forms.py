from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ContentForm(FlaskForm):
    content = TextAreaField('Content')
    submit = SubmitField('Update')


class OpenTimesForm(FlaskForm):
    cell_00 = TextAreaField('Monday Guests',validators=[DataRequired()])
    cell_01 = TextAreaField('Monday Public', validators=[DataRequired()])
    cell_10 = TextAreaField('Tuesday Guests', validators=[DataRequired()])
    cell_11 = TextAreaField('Tuesday Public', validators=[DataRequired()])
    cell_20 = TextAreaField('Wednesday Guests', validators=[DataRequired()])
    cell_21 = TextAreaField('Wednesday Public', validators=[DataRequired()])
    cell_30 = TextAreaField('Thursday Guests', validators=[DataRequired()])
    cell_31 = TextAreaField('Thursday Public', validators=[DataRequired()])
    cell_40 = TextAreaField('Friday Guests', validators=[DataRequired()])
    cell_41 = TextAreaField('Friday Public', validators=[DataRequired()])
    cell_50 = TextAreaField('Saturday Guests', validators=[DataRequired()])
    cell_51 = TextAreaField('Saturday Public', validators=[DataRequired()])
    cell_60 = TextAreaField('Sunday Guests', validators=[DataRequired()])
    cell_61 = TextAreaField('Sunday Public', validators=[DataRequired()])
    submit = SubmitField('Update')