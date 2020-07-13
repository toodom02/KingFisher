import os

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required

from flasksite import db
from flasksite.models import Post
from flasksite.posts.forms import PostForm
from flasksite.posts.utils import save_media

posts = Blueprint('posts', __name__)


@posts.route("/posts")
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('posts.html', posts=posts)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        media_file = []
        for file in form.media_file.data:
            if file.filename:
                media_file.append(save_media(file))
        post = Post(title=form.title.data, date=form.date.data, content=form.content.data, media_file=media_file,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.all_posts'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        try:
            for file in post.media_file:
                os.remove(os.path.join(current_app.root_path, 'static/post_media', file))
        except FileNotFoundError:
            pass

        media_file = []
        for file in form.media_file.data:
            if file.filename:
                media_file.append(save_media(file))

        post.title = form.title.data
        post.date = form.date.data
        post.content = form.content.data
        post.media_file = media_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.all_posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.date.data = post.date
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.media_file:
        for file in post.media_file:
            try:
                os.remove(os.path.join(current_app.root_path, 'static/post_media', file))
            except FileNotFoundError:
                pass
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.all_posts'))