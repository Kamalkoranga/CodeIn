from flask import render_template, flash, redirect, url_for, jsonify, request
from . import main
from flask_login import login_required, current_user
from .forms import PostForm, EditProfileForm
from ..models import Post, User, Like, Comment
from .. import db


@main.route('/feed', methods=['GET', 'POST'])
@login_required
def index():
    # Create an instance of the PostForm class
    form = PostForm()

    # Check if the form has been submitted and passes form validation
    if form.validate_on_submit():
        post = Post(
            body=form.body.data,
            post_name=form.post.data.filename,
            post_data=form.post.data.read(),
            author_id=current_user.id
        )

        # Add the new post to the database session
        db.session.add(post)

        # Commit the changes to the database
        db.session.commit()

        # Display a flash message to indicate successful posting
        flash('Posted Successfully')

        # Redirect the user to the 'index' endpoint
        return redirect(url_for('main.index'))

    # Retrieve all posts from the database in descending order of timestamp
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    # Retrieve all comments from the database
    comments = Comment.query.all()

    '''Render the 'index.html' template, passing the form, posts and comments
    to the template'''
    return render_template(
        'index.html', form=form, posts=posts, comments=comments
    )


@main.route("/image/<int:id>")
def get_image(id):
    """This route is only for retrieving images from the post

    Args:
        id (int): id of post

    Returns:
        image/jpeg: returns an image data
    """
    # Retrieve the post with the given ID from the database and uses as image
    image = Post.query.filter_by(id=id).first()

    # Return the post's image data as the response (image)
    return image.post_data, {"Content-Type": "image/jpeg"}


@main.route('/user/<username>')
def user(username):
    # Retrieve the user from the database based on the provided username
    user = User.query.filter_by(username=username).first_or_404()

    # Render the 'user.html' template and pass the user object to the template
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Create an instance of the EditProfileForm
    form = EditProfileForm()
    if form.validate_on_submit():

        # If the form is submitted and passes validation
        # Update the user's profile details with the form data
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        # Add the updated user object to the database session and commit the
        # changes
        db.session.add(current_user._get_current_object())
        db.session.commit()

        # Display a flash message to indicate successful profile update
        flash('Your profile has been updated.')

        # Redirect the user to their profile page
        return redirect(url_for('.user', username=current_user.username))

    # Populate the form fields with the current user's profile data
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.username.data = current_user.username

    # Render the 'edit_profile.html' template, passing the form object to the
    # template
    return render_template('edit_profile.html', form=form)


@main.route('/like_post/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    # Get the post object based on the provided post_id
    post = Post.query.filter_by(id=int(post_id)).first()

    # Check if the user has already liked the post
    like = Like.query.filter_by(
        author_id=current_user.id, post_id=post.id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        # If the user has already liked the post, remove the like
        db.session.delete(like)
        db.session.commit()
    else:
        # If the user has not liked the post, create a new like
        like = Like(author_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    res = {
        # Total number of likes for the post
        "likes": len(post.likes),

        # Check if the current user has liked the post
        "liked": current_user.id in map(lambda x: x.author_id, post.likes)
    }
    return jsonify(res)


@main.route('/add_comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    # Retrieve the post object based on the provided post_id
    post = Post.query.filter_by(id=int(post_id)).first()

    # Check if the post exists
    if not post:
        return jsonify({'error': 'post not found'})

    # Get the JSON data from the request
    data = request.get_json()

    # Create a new Comment object with the provided data
    comment = Comment(
        body=data['body'],
        author=current_user._get_current_object(),
        post_id=data['post_id']
    )

    # Add the comment to the database session
    db.session.add(comment)
    db.session.commit()

    # Return a JSON response indicating successful addition of the comment
    return jsonify({'msg': 'added'})
