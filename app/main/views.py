from flask import render_template, flash, redirect, url_for
from . import main
from flask_login import login_required, current_user
from .forms import PostForm, EditProfileForm
from ..models import Post, User
from .. import db


@main.route('/feed', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            body=form.body.data,
            post_name=form.post.data.filename,
            post_data=form.post.data.read(),
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Posted Successfully')
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


@main.route("/image/<int:id>")
def get_image(id):
    image = Post.query.filter_by(id=id).first()
    return image.post_data, {"Content-Type": "image/jpeg"}


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.username.data = current_user.username
    return render_template('edit_profile.html', form=form)
