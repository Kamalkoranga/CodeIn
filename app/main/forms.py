from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, StringField
from wtforms.validators import DataRequired, Length, Regexp
from ..models import User
from wtforms import ValidationError


class PostForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "What do you want to talk about?"})
    post = FileField('Add a photo')
    submit = SubmitField('Post')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')]
    )
    name = StringField('Full name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
