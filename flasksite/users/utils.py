import os
import secrets

from PIL import Image
from flask import current_app, render_template
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flasksite import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.html = render_template('reset_email.html', token=token, _external=True, user=user)
    mail.send(msg)


def send_request_email(username, forename, surname, email):
    msg = Message('Access Request', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[current_app.config['MAIL_USERNAME']])
    msg.html = render_template('access_email.html', _external=True, username=username, forename=forename,
                               surname=surname, email=email)
    mail.send(msg)


def send_register_email():
    token = get_register_token()
    msg = Message('Password Register Link', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[current_app.config['MAIL_USERNAME']])
    msg.html = render_template('register_email.html', token=token, _external=True)
    mail.send(msg)


def get_register_token(expires_seconds=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
    return s.dumps({'user_id': 0}).decode('utf-8')


def verify_register_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return False
    return True
