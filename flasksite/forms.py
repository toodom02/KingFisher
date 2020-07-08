from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flasksite.models import Staff


class RegistrationForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Staff.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Staff.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Staff.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Staff.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Staff.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today)
    content = TextAreaField('Content', validators=[DataRequired()])
    media_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class QuestionnaireForm(FlaskForm):
    q1 = TextAreaField('What services have you used at the Kingfisher Café?', validators=[DataRequired()])
    q2 = TextAreaField('How did this help you and your situation?', validators=[DataRequired()])
    q3 = TextAreaField('What services would you like to see the Kingfisher Café provide in the future?', validators=[DataRequired()])
    q4 = TextAreaField('How do you benefit by coming to the Kingfisher Café?', validators=[DataRequired()])
    q5 = TextAreaField('Would you consider volunteering at the Kingfisher Café?', validators=[DataRequired()])
    q6 = TextAreaField('If you have a good news story please tell us, the organisations that support our work need to hear that their contribution is benefiting you and our work in Bridlington.')
    submit = SubmitField('Submit')