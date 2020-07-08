import os
import secrets
import cv2

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from flasksite import app, db, bcrypt, mail
from flasksite.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm, PostForm, QuestionnaireForm)
from flasksite.models import Staff, Post

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


@app.route("/")
def home():
    posts = Post.query.order_by(Post.date.desc()).limit(2)
    return render_template('home.html', posts=posts)

@app.route("/questionnaire", methods=['GET', 'POST'])
def questionnaire():
    form = QuestionnaireForm()
    if form.validate_on_submit():

        flash('Questionnaire submitted. Thank You!', 'success')
        return redirect(url_for('questionnaire'))
    return render_template('questionnaire.html', title='Questionnaire', form=form)

@app.route("/posts")
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=5)
    return render_template('posts.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Staff(surname=form.surname.data, forename=form.forename.data, username=form.username.data,
                     email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Staff.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.jpg':
                try:
                    os.remove(os.path.join(app.root_path, 'static/profile_pics', current_user.image_file))
                except FileNotFoundError:
                    pass
            current_user.image_file = picture_file
        current_user.forename = form.forename.data
        current_user.surname = form.surname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.forename.data = current_user.forename
        form.surname.data = current_user.surname
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='kngfshr.reset@gmail.com', recipients=[user.email])
    msg.html = render_template('email.html', token=token, _external=True, user=user)
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Staff.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password',
            'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    staff = Staff.verify_reset_token(token)
    if staff is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        staff.password = hashed_password
        db.session.commit()
        flash('Password has been reset!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def save_media(form_media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_media.filename)
    media_fn = random_hex + f_ext
    media_path = os.path.join(app.root_path, 'static/post_media', media_fn)

    i = Image.open(form_media)
    i.save(media_path)


    return media_fn


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.media_file.data:
            media_file = save_media(form.media_file.data)
        else:
            media_file = None
        post = Post(title=form.title.data, date=form.date.data, content=form.content.data, media_file=media_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.media_file.data:
            media_file = save_media(form.media_file.data)
            os.remove(os.path.join(app.root_path, 'static/post_media', post.media_file))
        else:
            media_file = None
        post.title = form.title.data
        post.date = form.date.data
        post.content = form.content.data
        post.media_file = media_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.date.data = post.date
        form.content.data = post.content
        form.media_file.data = post.media_file
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.media_file:
        try:
            os.remove(os.path.join(app.root_path, 'static/post_media', post.media_file))
        except FileNotFoundError:
            pass
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts'))