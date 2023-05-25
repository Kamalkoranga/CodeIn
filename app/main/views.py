from flask import render_template, flash, redirect, url_for
from . import main
from flask_login import login_required, current_user
from .forms import PostForm
from ..models import Post
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
    posts = Post.query.all()
    return render_template('index.html', form=form, posts=posts)


@main.route("/image/<int:id>")
def get_image(id):
    image = Post.query.filter_by(id=id).first()
    return image.post_data, {"Content-Type": "image/jpeg"}
