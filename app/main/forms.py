from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "What do you want to talk about?"})
    post = FileField('Add a photo')
    submit = SubmitField('Post')
