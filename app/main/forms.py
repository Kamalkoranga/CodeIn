from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, StringField
from wtforms.validators import DataRequired, Length, Regexp
from ..models import User
from wtforms import ValidationError
from flask_login import current_user
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    # Define a form class for creating posts
    '''
        Create a TextAreaField named 'body' for the post content.
        The field is required, meaning it must have a value.
        The 'render_kw' parameter is used to provide additional attributes to
        the rendered HTML element.
        In this case, it adds a placeholder attribute to the field with the
        specified text.
    '''
    body = PageDownField(validators=[DataRequired()], render_kw={"placeholder": "What do you want to talk about?"})

    # Create a FileField named 'post' for uploading a photo
    # This field allows the user to select a file from their device
    post = FileField('Add a photo')

    # Create a SubmitField named 'submit' for submitting the form
    # This field represents a button that triggers the form submission
    submit = SubmitField('Post')


class EditProfileForm(FlaskForm):
    # Username field with validators
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')]
    )

    '''Full name and location field with length validator'''
    name = StringField('Full name', validators=[Length(0, 64)])
    headline = StringField('Headline', validators=[Length(0, 128)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')  # submit button

    def validate_username(self, field):
        # Custom validation for the username field
        user = User.query.filter_by(username=field.data).first()
        if user:
            if current_user != user:
                raise ValidationError('Username already in use.')


# Form for posting comment is done using html
