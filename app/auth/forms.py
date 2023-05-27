from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, StringField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError
from ..models import User


# Define login form fields
class LoginForm(FlaskForm):
    # Field for email input
    email = EmailField('Email',
                       validators=[DataRequired(), Email(), Length(1, 64)])
    # Field for password input
    password = PasswordField('Password', validators=[DataRequired()])
    # Submit button field
    submit = SubmitField('Sign in')


# Define signup form fields
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Join')

    # Custom validation method for the 'email' field
    def validate_email(self, field):
        # Check if the email already exists in the User table
        if User.query.filter_by(email=field.data.lower()).first():
            # Raise a validation error if the email is already registered
            raise ValidationError('Email already registered.')
