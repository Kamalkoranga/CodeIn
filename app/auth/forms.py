from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, StringField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
